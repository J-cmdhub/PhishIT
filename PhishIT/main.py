from core import create_app
import os
print("Current working directory:", os.getcwd())

app = create_app()

if __name__ == '__main__':
    # For development use; in production run via Gunicorn (e.g.: gunicorn -w 4 -b 0.0.0.0:5000 main:app)
    app.run(debug=True, use_reloader=False)
