import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

INTERP = "/virtualenv/tiendaMuhia/3.9/bin/python3.9"

environ=os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda.settings')

from tienda.wsgi import app
application = app

#def application(environ, start_response):
#    start_response('200 OK', [('Content-Type', 'text/plain')])
#    message = 'It works!\n'
#    version = 'Python %s\n' % sys.version.split()[0]
#    response = '\n'.join([message, version])
#    return [response.encode()]
