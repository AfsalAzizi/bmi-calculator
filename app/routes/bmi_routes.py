from flask import Blueprint, request, jsonify
from app.services.bmi_service import BMIService

bmi_bp = Blueprint('bmi', __name__)


@bmi_bp.route('/calculate-bmi', methods=['POST'])
def calculate_bmi():
    try:
        data = request.get_json()

        if not data or 'weight' not in data or 'height' not in data:
            return jsonify({'error': 'Missing weight or height in request'}), 400

        weight = float(data['weight'])
        height = float(data['height'])

        bmi = BMIService.calculate_bmi(weight, height)
        category = BMIService.get_bmi_category(bmi)

        return jsonify({
            'bmi': round(bmi, 2),
            'category': category,
            'weight': weight,
            'height': height
        })

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Invalid input'}), 400
