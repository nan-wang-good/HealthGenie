from flask import render_template, request, jsonify, current_app
from . import diet_bp
import requests
from concurrent.futures import ThreadPoolExecutor
import os
"""
This is a third-party api
"""
# TheMealDB API Configuration  
BASE_URL = os.getenv('MEALDB_URL', 'https://www.themealdb.com/api/json/v1/1')
TIMEOUT = 10  # seconds

def fetch_api_data(endpoint):
    """Thread-safe API fetcher with error handling"""
    try:
        response = requests.get(f'{BASE_URL}/{endpoint}', timeout=TIMEOUT)
        response.raise_for_status()
        return response.json().get('meals', [])
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"API Error ({endpoint}): {str(e)}")
        return {'error': str(e)}

@diet_bp.route('/')
def index():
    # Define endpoints to fetch in parallel
    endpoints = [
        'list.php?c=list',    # Categories
        'list.php?a=list',    # Areas
        'list.php?i=list'     # Ingredients
    ]
    
    # Execute all API calls in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(fetch_api_data, endpoints))
    
    # Handle partial failures
    errors = [r for r in results if isinstance(r, dict) and 'error' in r]
    if errors:
        current_app.logger.warning(f"Partial API failures: {errors}")
    
    return render_template(
        'diet/index.html',
        categories=results[0] if not isinstance(results[0], dict) else [],
        areas=results[1] if not isinstance(results[1], dict) else [],
        ingredients=results[2] if not isinstance(results[2], dict) else [],
        api_errors=errors
    )

@diet_bp.route('/filter')
def filter_meals():
    params = request.args.to_dict()
    if not params:
        return jsonify({'error': 'Missing filter parameters'}), 400
    
    # Determine filter type
    filter_type = next((k for k in ['c', 'a', 'i'] if k in params), None)
    if not filter_type:
        return jsonify({'error': 'Invalid filter parameter'}), 400
    
    try:
        # First fetch filtered meals
        meals = fetch_api_data(f'filter.php?{filter_type}={params[filter_type]}')
        if isinstance(meals, dict) and 'error' in meals:
            raise requests.exceptions.RequestException(meals['error'])
        
        if not meals:
            return jsonify({'meals': []})
            
        return jsonify({'meals': meals})
        
    except Exception as e:
        current_app.logger.error(f"Filter error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@diet_bp.route('/meal/<meal_id>')
def get_meal_details(meal_id):
    try:
        if not meal_id.isdigit():
            return jsonify({'error': 'Invalid meal ID'}), 400
            
        data = fetch_api_data(f'lookup.php?i={meal_id}')
        if isinstance(data, dict) and 'error' in data:
            raise requests.exceptions.RequestException(data['error'])
            
        if not data:
            return jsonify({'error': 'Meal not found'}), 404
            
        return jsonify(data[0])
        
    except Exception as e:
        current_app.logger.error(f"Meal lookup error: {str(e)}")
        return jsonify({'error': str(e)}), 500