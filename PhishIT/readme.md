# Flask Phishing Framework

## Setup Instructions

1. **Clone the Repository and Navigate to the Project Directory**
"git clone <repository_url> cd Flask-Phishing-Framework"

2. **Create a Virtual Environment and Activate It**

- On Windows:
  ```
  python -m venv venv
  venv\Scripts\activate
  ```
- On Linux/macOS:
  ```
  python3 -m venv venv
  source venv/bin/activate
  ```

3. **Install Dependencies**
`pip install -r requirements.txt`

4. **Configure Environment Variables (Optional)**
- Create a `.env` file to override default settings if needed.
- Example `.env`:
  ```
  SECRET_KEY=your_secret_key
  STORAGE_TYPE=json      # Or 'db' for SQLite
  JSON_STORAGE_PATH=logs/captured_data.json
  SQLITE_DB_PATH=logs/captured_data.db
  ```

5. **Run the Application**
- For development:
  ```
  python main.py
  ```
- For production, use a production-ready WSGI server like Gunicorn:
  ```
  gunicorn -w 4 -b 0.0.0.0:5000 main:app
  ```

6. **Access the Application**
- Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.
- Use the dashboard to select a phishing template.
- Visit `/admin` to view captured credentials.

## Tunneling
- To enable public hosting, you can use one of the tunneling scripts in the `tunnels/` folder.
- (These are currently stubs that return placeholder URLs; further development is needed to capture the actual public URL.)

## Notes
- This framework captures credentials and basic device information (via the User-Agent header) and stores them asynchronously.
- You can switch between JSON storage and SQLite by changing the `STORAGE_TYPE` in `core/config.py` (or via your environment variables).

## Future Enhancements
- Improve tunneling modules.
- Add advanced error handling and logging.
- Integrate a full background task queue if heavy load is expected.
