def check_health_risk(total_nutrition, age, weight, height):
    # Define thresholds for health risk based on nutritional values, age, and weight
    age_groups = {'Children': (0, 12), 'Adolescents': (13, 18), 'Adults': (19, 60), 'Elderly': (61, 150)}
    weight_status_thresholds = {'Underweight': 18.5, 'Normal': 24.9, 'Overweight': 29.9}

    # Function to determine weight status based on BMI
    def calculate_bmi(weight, height):
        print(weight/height**2)
        return (weight/height**2)

    # Calculate BMI using the provided height
    bmi_threshold = weight_status_thresholds['Normal']
    bmi = calculate_bmi(weight, height)

    # Determine age group
    for group, (lower, upper) in age_groups.items():
        if lower <= age <= upper:
            age_group = group
            break
    else:
        age_group = None

    # Check weight status
    if bmi < weight_status_thresholds['Underweight']:
        weight_status = 'Underweight'
    elif bmi < weight_status_thresholds['Normal']:
        weight_status = 'Normal'
    else:
        weight_status = 'Overweight'

    # Check health risk based on age, weight status, and nutritional values
    health_risk = []

    if age_group:
        if age_group == 'Children':
            if total_nutrition['Protein'] < 20 or total_nutrition['Calories'] < 1200:
                health_risk.append('Stunted growth, developmental delays')

        elif age_group == 'Adolescents':
            if total_nutrition['Protein'] < 45 or total_nutrition['Calories'] < 1800:
                health_risk.append('Stunted growth, developmental delays')

        elif age_group == 'Adults':
            if weight_status == 'Underweight' and total_nutrition['Protein'] < 50:
                health_risk.append('Nutritional deficiencies, weakened immune system')
            elif weight_status == 'Overweight':
                health_risk.append('Increased risk of chronic diseases')

        elif age_group == 'Elderly':
            if weight_status == 'Underweight' and total_nutrition['Protein'] < 50:
                health_risk.append('Nutritional deficiencies, weakened immune system')
            elif weight_status == 'Overweight':
                health_risk.append('Increased risk of chronic diseases')

    return health_risk

# Example usage with user input
# user_age = int(input("Enter your age: "))
# user_weight = float(input("Enter your weight in kilograms: "))
# user_height = float(input("Enter your height in meters: "))

# Check health risk based on total nutrition, age, weight, and height
# health_risk = check_health_risk(total_nutrition, user_age, user_weight, user_height)

# Display health risk information
# if health_risk:
#     for risk in health_risk:
#         print(f"- {risk}")
# else:
#     print("No significant health risks identified.")