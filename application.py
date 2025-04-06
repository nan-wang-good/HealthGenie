from flask import Flask, render_template, session, redirect, url_for, request
from config import Config
from flask_login import LoginManager, current_user
from models.user import User
from blueprints.auth import auth_bp
from blueprints.diet import diet_bp
from blueprints.fitness import fitness_bp
from blueprints.weather import weather_bp
from blueprints.exchange import exchange_bp
from db import db, init_db
from flask_cors import CORS
# Flask Application Initialization (Loading Configuration)
application = Flask(__name__)
CORS(application)
application.config.from_object(Config)

# Initial SQLAlchemy
init_db(application)

# Initialize Flask-Login (User Authentication Management)
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = 'auth.login'  # Set up the login view endpoint

# User loader (fetches user object based on ID)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Whitelist route list
WHITELIST_ROUTES = ['index', 'static', 'auth.login', 'auth.register', 'auth.forgot_password', 'auth.reset_password']

# Global Route Interceptor
@application.before_request
def check_login():
    # Get the current route endpoint
    endpoint = request.endpoint
    
    # If the route is whitelisted, the route is allowed directly
    if endpoint in WHITELIST_ROUTES:
        return
    
    # Check if the user is logged in
    if not session.get('user_email'):
        return redirect(url_for('auth.login'))

# Enrollment Blueprint (Modular Routing)
application.register_blueprint(auth_bp, url_prefix='/auth')
application.register_blueprint(diet_bp, url_prefix='/diet')
application.register_blueprint(fitness_bp, url_prefix='/fitness')
application.register_blueprint(weather_bp, url_prefix='/weather')
application.register_blueprint(exchange_bp, url_prefix='/exchange')

# Context Processor (injecting session data into the template)
@application.context_processor
def inject_user():
    return dict(
        user_email=session.get('user_email'),  # The current user's email address
        nickname=session.get('nickname')       # The current user's nickname
    )

@application.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    application.run(threaded = True, host='0.0.0.0', port=8080)