import subprocess
import logging


def start_localtunnel():
    try:
        process = subprocess.Popen(["lt", "--port", "5000"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "https://your-localtunnel-url.com"
    except Exception as e:
        logging.exception("Error starting LocalTunnel")
        return None
