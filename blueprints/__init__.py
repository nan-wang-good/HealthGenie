from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
fitness_bp = Blueprint('fitness', __name__)
diet_bp = Blueprint('diet', __name__)
weather_bp = Blueprint('weather', __name__)
exchange_bp = Blueprint('exchange', __name__)

from . import auth, fitness, diet, weather, exchange