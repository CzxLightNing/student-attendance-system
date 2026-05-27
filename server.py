import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Note: staticfiles/ directory is handled by Django's collectstatic and excluded via .gitignore.
# No need to serve static files separately with Waitress.
from waitress import serve
from config.wsgi import application

if __name__ == '__main__':
    host = os.getenv('WAITRESS_HOST', '0.0.0.0')
    port = int(os.getenv('WAITRESS_PORT', '8000'))
    threads = int(os.getenv('WAITRESS_THREADS', '8'))
    channel_timeout = int(os.getenv('WAITRESS_CHANNEL_TIMEOUT', '120'))

    print(f'Starting Waitress server on {host}:{port} (threads={threads})')
    serve(
        application,
        host=host,
        port=port,
        threads=threads,
        channel_timeout=channel_timeout,
    )
