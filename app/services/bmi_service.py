class BMIService:
    @staticmethod
    def calculate_bmi(weight_kg, height_m):
        """Calculate BMI given weight in kg and height in meters."""
        if weight_kg <= 0 or height_m <= 0:
            raise ValueError("Weight and height must be positive numbers")
        return weight_kg / (height_m ** 2)

    @staticmethod
    def get_bmi_category(bmi):
        """Get BMI category based on BMI value."""
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
