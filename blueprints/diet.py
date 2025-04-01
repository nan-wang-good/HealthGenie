from flask import render_template, request, jsonify
from . import diet_bp
import requests

# TheMealDB APIBasicURL   ---Third Party API
BASE_URL = 'https://www.themealdb.com/api/json/v1/1'

@diet_bp.route('/')
def index():
    # Get taxonomic, regional, and ingredient data
    categories_response = requests.get(f'{BASE_URL}/list.php?c=list', proxies=None)
    areas_response = requests.get(f'{BASE_URL}/list.php?a=list', proxies=None)
    ingredients_response = requests.get(f'{BASE_URL}/list.php?i=list', proxies=None)
    
    # Extract data
    categories = categories_response.json().get('meals', [])
    areas = areas_response.json().get('meals', [])
    ingredients = ingredients_response.json().get('meals', [])
    
    return render_template('diet/index.html',
                           categories=categories,
                           areas=areas,
                           ingredients=ingredients)


@diet_bp.route('/filter.php')
def filter_meals():
    # Get the query parameters
    category = request.args.get('c')  # Filter by category
    area = request.args.get('a')      # Filter by region
    ingredient = request.args.get('i') # Filter by ingredients
    
    # Decide which query parameter to use
    if category:
        filter_param = ('c', category)
    elif area:
        filter_param = ('a', area)
    elif ingredient:
        filter_param = ('i', ingredient)
    else:
        return jsonify({'error': 'Missing filter parameters'}), 400
    
    try:
        # Build an API request URL
        response = requests.get(f'{BASE_URL}/filter.php?{filter_param[0]}={filter_param[1]}', proxies=None)
        response.raise_for_status()
        return jsonify(response.json()), 200, {'Content-Type': 'application/json'}
    except requests.RequestException as e:
        return jsonify({'error': f'API request failed: {str(e)}'}), 500

@diet_bp.route('/meal/<meal_id>')
def get_meal_details(meal_id):
    response = requests.get(f'{BASE_URL}/lookup.php?i={meal_id}', proxies=None)
    return jsonify(response.json())