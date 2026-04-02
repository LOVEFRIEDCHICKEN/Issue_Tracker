from datetime import timedelta
from flask import Flask, render_template
from flask_cors import CORS
from config import Config
from controllers.auth_controller import login_manager, auth_bp
from controllers.issue_controller import issue_bp
from controllers.admin_controller import admin_bp

def create_app():
    flask_app = Flask(__name__) # create flask app object + set route
    flask_app.config.from_object(Config) # load .env setting

    # login_manager initialize
    login_manager.init_app(flask_app)
    login_manager.login_view = 'auth.login' # if fail to log in, redirect to /auth/login

    # templates/static folder
    flask_app.template_folder = 'templates'
    flask_app.static_folder = 'static'

    # Register Blueprint
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(issue_bp)
    flask_app.register_blueprint(admin_bp)

    CORS(flask_app) # allow to call api

    flask_app.permanent_session_lifetime = timedelta(seconds=flask_app.config['PERMANENT_SESSION_LIFETIME'])


    @flask_app.route('/')
    def health_check():
        return render_template('index.html')
        # return {'Message': 'Issue Tracker API is on running', 'version': '1.0.0'}

    return flask_app


if __name__ == '__main__':
    app = create_app()
    app.run(debug = True, host = '0.0.0.0', port = 5000)

