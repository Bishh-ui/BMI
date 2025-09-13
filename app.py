from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def calculate_bmi(weight_kg, height_m):
    """Calculate BMI."""
    return weight_kg / (height_m ** 2)

def calculate_body_fat(bmi, age, sex):
    """Estimate body fat percentage using Deurenberg formula."""
    if sex.lower() == 'male':
        return (1.20 * bmi) + (0.23 * age) - 16.2
    else:
        return (1.20 * bmi) + (0.23 * age) - 5.4

def calculate_bmr(weight_kg, height_m, age, sex):
    """Calculate BMR using Mifflin-St Jeor Equation."""
    height_cm = height_m * 100  # Convert meters to cm for BMR formula
    if sex.lower() == 'male':
        return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

def get_bmi_category(bmi):
    """Return BMI category and health risk."""
    if bmi < 18.5:
        return "Underweight", "Risk of nutritional deficiency; consult a dietitian."
    elif 18.5 <= bmi <= 24.9:
        return "Normal weight", "Low health risk; maintain healthy habits."
    elif 25 <= bmi <= 29.9:
        return "Overweight", "Increased risk of cardiovascular issues; consider lifestyle changes."
    else:
        return "Obesity", "High risk of diabetes, heart disease; seek medical advice."

def get_recommendations(bmi):
    """Provide personalized recommendations."""
    if bmi < 18.5:
        return "Consider a balanced diet to gain healthy weight. Consult a nutritionist."
    elif 25 <= bmi:
        return "Incorporate regular exercise and a balanced diet. Consult a healthcare provider."
    else:
        return "Maintain your current healthy lifestyle!"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            weight_kg = float(request.form['weight'])
            height_feet = float(request.form['height'])
            age = int(request.form['age'])
            sex = request.form['sex'].lower()

            # Input validation
            if weight_kg <= 0 or height_feet <= 0 or age <= 0:
                return render_template('index.html', error="Weight, height, and age must be positive.")
            if sex not in ['male', 'female']:
                return render_template('index.html', error="Sex must be 'male' or 'female'.")

            # Convert height to meters
            height_m = height_feet * 0.3048

            # Calculate metrics
            bmi = calculate_bmi(weight_kg, height_m)
            body_fat = calculate_body_fat(bmi, age, sex)
            bmr = calculate_bmr(weight_kg, height_m, age, sex)
            category, risk = get_bmi_category(bmi)
            recommendations = get_recommendations(bmi)

            # Chart.js data
            chart_data = {
                "labels": ["Underweight", "Normal", "Overweight", "Obesity"],
                "ranges": [18.5, 24.9, 29.9, 40],
                "user_bmi": round(bmi, 1)
            }

            return render_template(
                'results.html',
                bmi=round(bmi, 1),
                body_fat=round(body_fat, 1),
                bmr=round(bmr),
                category=category,
                risk=risk,
                recommendations=recommendations,
                chart_data=chart_data
            )

        except ValueError:
            return render_template('index.html', error="Please enter valid numeric values for weight, height, and age.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
