import subprocess
import logging


def start_cloudflared():
    try:
        process = subprocess.Popen(["cloudflared", "tunnel", "--url", "localhost:5000"], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        return "https://your-cloudflared-url.com"
    except Exception as e:
        logging.exception("Error starting Cloudflared tunnel")
        return None
