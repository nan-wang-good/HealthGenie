from . import exchange_bp
from flask import Blueprint, render_template, request, jsonify
import requests
from datetime import datetime
"""
This API from from classmate     ---23340355
"""

# API config
API_BASE_URL = 'https://2430zel9za.execute-api.eu-west-1.amazonaws.com/prod'

@exchange_bp.route('/')
def index():
    return render_template('exchange/index.html')

@exchange_bp.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.get_json()
        
        # check fields
        required_fields = ['amount', 'from_currency', 'to_currency']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # call API
        response = requests.post(
            f'{API_BASE_URL}/convert',
            json={
                'amount': float(data['amount']),
                'from_currency': data['from_currency'],
                'to_currency': data['to_currency']
            },
            timeout=10
        )
        response.raise_for_status()
        
        return jsonify(response.json())
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'API request failed: {str(e)}'}), 500
    except ValueError:
        return jsonify({'error': 'Invalid amount format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@exchange_bp.route('/exchange-rate/<from_currency>/<to_currency>')
def get_rate(from_currency, to_currency):
    try:
        response = requests.get(
            f'{API_BASE_URL}/exchange-rate/{from_currency}/{to_currency}',
            timeout=10
        )
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500