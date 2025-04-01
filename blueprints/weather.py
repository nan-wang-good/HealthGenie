from flask import render_template, jsonify
from . import weather_bp
#Api uses mock data combined with 'OpenWeatherMap' to return weather data to return weather information.

@weather_bp.route('/')
def index():
    return render_template('weather/index.html')

@weather_bp.route('/current')
def get_current_weather():
    # Mock current weather data
    # TODO: Replace with actual weather API integration
    weather_data = {
        'temperature': 25,
        'description': 'Sunny',
        'humidity': 60,
        'wind_speed': 3.5,
        'icon_url': 'https://openweathermap.org/img/wn/01d@2x.png',
        'forecast': [
            {
                'date': 'Tomorrow',
                'temp_max': 27,
                'temp_min': 18,
                'description': 'Cloudy',
                'icon_url': 'https://openweathermap.org/img/wn/02d@2x.png'
            },
            {
                'date': 'Day After Tomorrow',
                'temp_max': 26,
                'temp_min': 17,
                'description': 'Sunny',
                'icon_url': 'https://openweathermap.org/img/wn/01d@2x.png'
            },
            {
                'date': 'In 3 Days',
                'temp_max': 24,
                'temp_min': 16,
                'description': 'Light Rain',
                'icon_url': 'https://openweathermap.org/img/wn/10d@2x.png'
            }
        ],
        'air_quality': {
            'aqi': 45,
            'level': 'Good',
            'pm25': 15,
            'pm10': 28,
            'no2': 25,
            'so2': 8
        },
        'suggestions': {
            'uv_index': 'Moderate',
            'uv_advice': 'Sunscreen recommended',
            'sports_advice': 'Suitable for outdoor activities',
            'comfort_level': 'Comfortable'
        }
    }
    
    return jsonify(weather_data)