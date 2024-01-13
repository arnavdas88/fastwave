import pathlib, typing

# FaseAPI
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.types import DecoratedCallable

from h2o_lightwave_web import web_directory

from fastwave.utils import search_if_route_exist, select_route_from_app_by_name


from fastwave.context import Global
from fastwave.core import WaveFunc

# Define a global buffer to maintain a Wave UI registry
context = Global()
context.registry: typing.List[WaveFunc] = []

def wave(func: typing.Union[typing.Callable, DecoratedCallable]):
    # Build a WaveFunc object
    _f = WaveFunc(func)
    # Register into global buffer
    context.registry.append(_f)
    # Returns the HTML render of the ui
    return _f.to_html_render()

def wave_collector(app: FastAPI):

    # For all WaveFunc object in the global buffer
    for _f in context.registry:
        # Assign WebSocket Path
        route = select_route_from_app_by_name(app, _f.name)
        if route.path.startswith('/'):
            _f.socket_path = "/ws" + route.path
        else:
            _f.socket_path = "/ws/" + route.path
        
        # Register the WebSocket into FastAPI
        app.websocket(_f.socket_path)(_f.to_ws_worker())

        # If static resources not mounted previously, mount them now
        if not search_if_route_exist(app, _f.assets_path):
            static_files = StaticFiles(directory=web_directory, html=True)
            app.mount(_f.assets_path, static_files, name=_f.assets_path)
