from flask import Flask, request, jsonify

app = Flask(__name__)


def calculate_bmi(weight_kg, height_m):
    """Calculate BMI given weight in kg and height in meters."""
    if weight_kg <= 0 or height_m <= 0:
        raise ValueError("Weight and height must be positive numbers")
    return weight_kg / (height_m ** 2)


@app.route('/calculate-bmi', methods=['POST'])
def bmi_calculator():
    try:
        data = request.get_json()

        if not data or 'weight' not in data or 'height' not in data:
            return jsonify({'error': 'Missing weight or height in request'}), 400

        weight = float(data['weight'])
        height = float(data['height'])

        bmi = calculate_bmi(weight, height)

        return jsonify({
            'bmi': round(bmi, 2),
            'weight': weight,
            'height': height
        })

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Invalid input'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
