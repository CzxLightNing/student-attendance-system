import os
import sys
from dotenv import load_dotenv
from waitress import serve
from config.wsgi import application

load_dotenv()

HOST = os.getenv('WAITRESS_HOST', '0.0.0.0')
PORT = int(os.getenv('WAITRESS_PORT', '8000'))
THREADS = int(os.getenv('WAITRESS_THREADS', '8'))
CHANNEL_TIMEOUT = int(os.getenv('WAITRESS_CHANNEL_TIMEOUT', '120'))

print(f'Starting Waitress server on {HOST}:{PORT} (threads={THREADS})')

serve(
    application,
    host=HOST,
    port=PORT,
    threads=THREADS,
    channel_timeout=CHANNEL_TIMEOUT,
)
