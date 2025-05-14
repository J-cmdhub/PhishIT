import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    # STORAGE_TYPE can be 'json' (default) or 'db' for SQLite
    STORAGE_TYPE = os.environ.get('STORAGE_TYPE') or 'json'
    JSON_STORAGE_PATH = os.environ.get('JSON_STORAGE_PATH') or 'logs/captured_data.json'
    SQLITE_DB_PATH = os.environ.get('SQLITE_DB_PATH') or 'logs/captured_data.db'
