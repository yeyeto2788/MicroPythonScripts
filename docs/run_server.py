"""
Simple script to run the server on a given ip and port by the `config`
variable on this file.

It uses waitress to handle all WSGI related.
"""
from waitress import serve

from docs.presentation_server import app

# Configuration of the server
config = {'ip': '0.0.0.0', 'port': 80}

# Generate a new Key with os.urandom(16) if you want to change it.
app.secret_key = '3ZX\xb336\x15\x82/\xd5N1O\n\x9f\x8a'

if __name__ == "__main__":
    serve(app, listen='{}:{}'.format(config['ip'], config['port']))
