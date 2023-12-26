# Core python packages
import pathlib, os, re

# H2O LightWave for Web
# from h2o_lightwave_web import get_web_files
from h2o_lightwave_web import web_directory


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