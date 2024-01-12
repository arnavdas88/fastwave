import pathlib, typing

# FaseAPI
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

# Jinja Template Engine
from jinja2 import Environment, FileSystemLoader

from starlette.background import BackgroundTask

from h2o_wave.server import HandleAsync, Query

from h2o_lightwave.server import _App

from h2o_lightwave_web import web_directory

from fastwave.utils import get_web_files, search_if_route_exist

fastwave_web_dir = str(pathlib.Path(__file__).parent / 'www')

# Prepare our custom index.html and inject required JS files.
# Jinja is used for convenience, you can use any templating engine.
template = Environment(loader=FileSystemLoader(fastwave_web_dir)).get_template("index_template.html")

class H2O_WaveUI:
    def __init__(self, app, name:str, assets_path:str = "/assets"):
        self.app = app
        self.name = name
        self.socket_path = f"/ws/{self.name}/"
        self.assets_path = assets_path

        self.socket_built:bool = False

        self.__bind__()
    
    def __bind__(self, ):
        if search_if_route_exist(self.app, self.assets_path):
            return
        static_files = StaticFiles(directory=web_directory, html=True)
        self.app.mount(self.assets_path, static_files, name=self.assets_path)

    def __call__(self, func: typing.Callable[typing.Any, HandleAsync]):
        if not self.socket_built:
            self.app.websocket(self.socket_path)(self.socker_gen(func))
            self.socket_built = True

        def static_callable_base():
            return self.callable_base_render()
        
        # static_callable_base.__name__ = f"H2O Wave UI for {self.name}"
        static_callable_base.__name__ = func.__name__
        if func.__doc__ is None:
            static_callable_base.__doc__  = f"H2O Wave UI for {self.name}. Served through the socket `{self.socket_path}`"
        else:
            static_callable_base.__doc__  = func.__doc__
        static_callable_base.__module__ = func.__module__

        return static_callable_base

    def callable_base_render(self, ):
        return HTMLResponse(template.render(wave_files=get_web_files(self.assets_path, True), data_wave_socket_url = self.socket_path))
    
    def socker_gen(self, serve):
        
        async def ws(ws: WebSocket):
            try:
                await ws.accept()


                # Hook Lightwave by importing "wave_serve" function and
                # passing our "serve" function with counter app.

                # For lightwave
                # await wave_serve(serve, ws.send_text, ws.receive_text)
                # OR
                await _App(serve, ws.send_text, ws.receive_text)._run()


                await ws.close()
            except WebSocketDisconnect:
                print('Client disconnected')
        
        return ws