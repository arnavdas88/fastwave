# Core python packages
import pathlib, os, re
import typing
import functools
import inspect

# H2O LightWave
from h2o_lightwave import Q as LightwaveQ
from h2o_wave import Q as WaveQ
# H2O LightWave for Web
# from h2o_lightwave_web import get_web_files
from h2o_lightwave_web import web_directory

from fastapi import FastAPI, WebSocket


# NOTE: Overriding the "relative" path to "absolute" path
# TODO: Inject web_files to this file during build time. No need to read index.html at runtime.
def get_web_files(prefix: str = '', absolute: bool = False) -> str:
    if prefix:
        if not prefix.endswith('/'):
            prefix += '/'
        if prefix.startswith('/'):
            prefix = prefix[1:]

    find_str = './wave-static/' if absolute else '/wave-static/'
    web_files = []
    with open(os.path.join(web_directory, 'index.html'), 'r') as f:
        for line in f:
            stripped_line = line.strip()
            if re.search(r'(\.js|\.css)(\'|\")', stripped_line):
                web_files.append(stripped_line.replace(find_str, f'/{prefix}wave-static/'))
    web_files = '\n'.join(web_files)

    return web_files

def search_if_route_exist(app, route_name):
    # route_list = [ route for route in self.app.router.routes ]
    route_name_list = [ route.name for route in app.router.routes ]
    return (route_name in route_name_list)

def change_signature(original_function, new_parameters):
    # Get the original function's signature
    original_signature = inspect.signature(original_function)

    # Create a new list of parameters
    new_params = [
        inspect.Parameter(name, inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=param_type)
        for name, param_type in new_parameters
    ]

    # Create a new signature with the updated parameters
    new_signature = original_signature.replace(parameters=new_params)

    @functools.wraps(original_function)
    def wrapper(*args, **kwargs):
        # Bind the arguments to the new signature
        bound_args = new_signature.bind(*args, **kwargs)
        bound_args.apply_defaults()

        # Call the original function with the updated arguments
        return original_function(**bound_args.arguments)
    wrapper.__signature__ = new_signature
    wrapper.__annotations__ = dict(new_parameters)

    return wrapper

def type_support_pydantic(obj, exclude_types:typing.List[typing.Any] = []):
    if obj in [WaveQ, LightwaveQ, *exclude_types]:
        return False
    return True

def select_route_from_app_by_name(app:FastAPI, definition_name: str):
    for route in app.routes:
        if route.name == definition_name:
            return route
    raise Exception("")

def get_parameters(func:typing.Callable, exclude_types:typing.List[typing.Any] = []):
    func_signature: inspect.Signature = inspect.signature(func)
    func_parameters: typing.OrderedDict = func_signature.parameters
    allowed_parameters: typing.List[typing.Tuple[str, typing.Any]] = [ (key, values.annotation) for (key, values) in  func_parameters.items() if type_support_pydantic(values.annotation, exclude_types)]
    return (func_parameters, allowed_parameters)

def takes_websocket_as_input_parameter(func:typing.Callable) -> bool:
    for param_name, _ in list(filter(lambda x:x[1] is WebSocket, func.__annotations__.items())):
        return param_name
    return False
