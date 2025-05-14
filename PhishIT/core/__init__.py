# from flask import Flask
# from core.routes import bp as main_blueprint
# from core.config import Config
#
# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)
#     app.register_blueprint(main_blueprint)
#     return app

# from flask import Flask
#
#
# def create_app():
#     app = Flask(__name__, template_folder="templates")
#     app.config.from_object("core.config.Config")
#     from core.routes import bp as main_blueprint
#     app.register_blueprint(main_blueprint)
#     return app

from flask import Flask


# import os
# print("Current working directory:", os.getcwd())

def create_app():
    # Explicitly set template_folder relative to the working directory
    app = Flask(__name__, template_folder='C:\\Users\\jatin\\PycharmProjects\\Phisingprject\\PhishIT\\templates')
    app.config.from_object("core.config.Config")
    from core.routes import bp as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
