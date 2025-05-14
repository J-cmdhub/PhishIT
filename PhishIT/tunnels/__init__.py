from .ngrok_tunnel import start_ngrok
# Optionally, import others:
# from .localtunnel import start_localtunnel
# from .cloudflared import start_cloudflared

def start_tunnel(service):
    if service == "ngrok":
        return start_ngrok()
    # Extend for other services if desired
    else:
        return None
