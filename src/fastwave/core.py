import inspect
import pathlib
import typing

# FaseAPI
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.types import DecoratedCallable
from h2o_lightwave import Q, data
from h2o_lightwave.server import _App
from h2o_wave.server import HandleAsync, Query

# Jinja Template Engine
from jinja2 import Environment, FileSystemLoader
from starlette.background import BackgroundTask

from fastwave.utils import (
    change_signature,
    get_parameters,
    get_web_files,
    takes_websocket_as_input_parameter,
    type_support_pydantic,
)

fastwave_web_dir = str(pathlib.Path(__file__).parent / "www")

# Prepare our custom index.html and inject required JS files.
# Jinja is used for convenience, you can use any templating engine.
template = Environment(loader=FileSystemLoader(fastwave_web_dir)).get_template(
    "index_template.html"
)

# Custom dictionary to safely format strings for rendering templates
class SafeDict(dict):
    # https://stackoverflow.com/a/17215533
    def __missing__(self, key):
        return "{" + key + "}"


class WaveFunc:
    def __init__(self, func: typing.Callable):
        self.name = func.__name__
        self.func = func
        self.assets_path: str = "/assets"
        self.socket_path: str = f"/ws/{self.func.__name__}/"

        # Initialize placeholders for WebSocket and HTML rendering handles
        self.ws: typing.Callable = None
        self.html_render: typing.Callable = None

    def __call__(
        self,
    ):
        pass

    def to_html_render(
        self,
    ):
        # Create and return an HTML rendering handle for the WaveFunc object
        def wrapper(*args, **kwargs):
            return HTMLResponse(
                template.render(
                    wave_files=get_web_files(self.assets_path, True),
                    data_wave_socket_url=self.socket_path.format_map(
                        SafeDict(**kwargs)
                    ),
                )
            )

        # Override function name
        wrapper.__name__ = self.func.__name__

        # Override function documentation
        if self.func.__doc__ is None:
            wrapper.__doc__ = f"H2O Wave UI for {self.func.__name__}. Served through the socket (Possibly: `{self.socket_path}`)"
        else:
            wrapper.__doc__ = self.func.__doc__

        # Override function's parent module
        wrapper.__module__ = self.func.__module__

        # Override function's param signature, safely
        func_parameters, allowed_parameters = get_parameters(
            self.func, exclude_types=[WebSocket]
        )
        self.html_render = change_signature(wrapper, allowed_parameters)

        return self.html_render

    def to_ws_worker(
        self,
    ):
        # Create and return a WebSocket worker handle for the WaveFunc object
        async def ws(ws: WebSocket, *args, **kwargs):
            try:
                # Define a wrapper function to handle WebSocket communication
                def wrapper(q: Q):
                    ws_parameter_name = takes_websocket_as_input_parameter(self.func)
                    if ws_parameter_name:
                        return self.func(
                            q=q, *args, **kwargs, **{ws_parameter_name: ws}
                        )
                    else:
                        return self.func(q=q, *args, **kwargs)

                await ws.accept()

                # Hook Lightwave by importing "wave_serve" function and
                # passing our "serve" function with counter app.

                # For lightwave
                # await wave_serve(self.func, ws.send_text, ws.receive_text)
                # OR
                await _App(wrapper, ws.send_text, ws.receive_text)._run()

                await ws.close()
            except WebSocketDisconnect:
                print("Client disconnected")

        # Override function's param signature, safely
        _, allowed_parameters_original = get_parameters(
            self.func, exclude_types=[Request, WebSocket]
        )
        wrapped_annotations = ws.__annotations__
        self.ws = change_signature(
            ws, set(allowed_parameters_original + list(wrapped_annotations.items()))
        )

        return self.ws
