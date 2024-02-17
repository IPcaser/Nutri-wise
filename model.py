import pandas as pd

import numpy as np
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load the dataset
file_path = r'nutrients.xlsx'
df = pd.read_excel(file_path)

# Function to calculate nutritional values for user input
def calculate_nutrition(user_input):

    total_nutrition = {'Calories': 0, 'Protein': 0, 'Fat': 0, 'Fiber': 0, 'Carbs': 0}

    for food, quantity in user_input.items():
        # Remove leading/trailing spaces and handle the extra space in the column name
        food_info = df[df['Food'].str.strip() == food.strip()]

        # Check if any rows are returned
        if not food_info.empty:
            food_info = food_info.iloc[0]  # Access the first (and only) row

            # Convert 'Grams' column to numeric
            grams = pd.to_numeric(food_info['Grams'], errors='coerce')

            if not pd.isnull(grams):
                for nutrient in total_nutrition.keys():
                    # Convert nutrient values to numeric
                    nutrient_value = pd.to_numeric(food_info[nutrient], errors='coerce')
                    if not pd.isnull(nutrient_value):
                        total_nutrition[nutrient] += (quantity / grams) * nutrient_value
                    else:
                        print(f"Invalid nutrient value for {nutrient} in {food}.")
            else:
                print(f"Invalid 'Grams' value for {food}.")
        else:
            print(f"No information found for {food}.")

    return total_nutrition

# Function to recommend a balanced diet based on total nutrition
def recommend_diet(total_nutrition):
    # Define the recommended ranges for each nutrient
    recommended_ranges = {
        'Protein': {'min': 50, 'max': 150},
        'Fat': {'min': 30, 'max': 70},
        'Fiber': {'min': 25, 'max': 40},
        'Carbs': {'min': 130, 'max': 300}
    }

    # Print the calculated nutrition values
    a = [total_nutrition['Calories'], total_nutrition['Protein'], total_nutrition['Fat'], total_nutrition['Fiber'], total_nutrition['Carbs']]



    # print("Calories:", total_nutrition['Calories'])
    # print("Protein:", total_nutrition['Protein'])
    # print("Fat:", total_nutrition['Fat'])
    # print("Fiber:", total_nutrition['Fiber'])
    # print("Carbs:", total_nutrition['Carbs'])

    # Create horizontal bar charts
    nutrients = list(total_nutrition.keys())
    values = list(total_nutrition.values())
    min_ranges = [recommended_ranges[nutrient]['min'] for nutrient in nutrients if nutrient != 'Calories']
    max_ranges = [recommended_ranges[nutrient]['max'] for nutrient in nutrients if nutrient != 'Calories']

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))

    # Bar chart for consumed, recommended min, and recommended max values
    bar_width = 0.2
    index = np.arange(len(nutrients) - 1)

    consumed = ax1.bar(index, values[1:], bar_width, label='Consumed')
    recommended_min = ax1.bar(index + bar_width, min_ranges, bar_width, label='Recommended Min')
    recommended_max = ax1.bar(index + 2 * bar_width, max_ranges, bar_width, label='Recommended Max')

    ax1.set_xlabel('Amount (g)')
    ax1.set_title('Nutritional Distribution (excluding Calories)')
    ax1.set_xticks(index + bar_width)
    ax1.set_xticklabels(nutrients[1:])
    ax1.legend()

    # Add text annotations for consumed values
    for i, val in enumerate(values[1:]):
        ax1.text(i, val, str(round(val, 2)), ha='center', color='black', fontweight='bold')

    # Donut chart
    labels = [label for label in total_nutrition.keys() if label != 'Calories']
    sizes = [total_nutrition[label] for label in labels]
    explode = (0.1, 0, 0, 0)  # Explode the first slice (Protein)

    # Define colors for each nutrient
    colors = plt.cm.Set3(range(len(labels)))

    wedges, texts, autotexts = ax2.pie(sizes, labels=labels, startangle=140,
                                       colors=colors, wedgeprops=dict(width=0.4, edgecolor='w'),
                                       autopct='%1.1f%%', explode=explode)

    # Draw a circle in the center to create a donut chart
    centre_circle = plt.Circle((0, 0), 0.2, color='white', edgecolor='black', linewidth=0.8)
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Add legend for the donut chart
    ax2.legend(wedges, labels, title="Nutrients", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax2.set_title('Nutritional Distribution (excluding Calories)')

    # plt.show()
    bar_chart_path = 'static/img/bar_chart.png'
    donut_chart_path = 'static/img/donut_chart.png'

    # Save bar chart
    fig, ax = plt.subplots()
    ax.bar(index, values[1:], bar_width, label='Consumed')
    ax.bar(index + bar_width, min_ranges, bar_width, label='Recommended Min')
    ax.bar(index + 2 * bar_width, max_ranges, bar_width, label='Recommended Max')
    ax.set_xlabel('Amount (g)')
    ax.set_title('Nutritional Distribution (excluding Calories)')
    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(nutrients[1:])
    ax.legend()
    ax.set_title('Nutritional Distribution (excluding Calories)')
    plt.savefig(bar_chart_path)
    plt.close()

    # Save donut chart
   # Save donut chart with adjusted position
    fig, ax = plt.subplots()  # Adjust the figsize as needed
    ax.pie(sizes, labels=labels, startangle=140, colors=colors,
           wedgeprops=dict(width=0.4, edgecolor='w'), autopct='%1.1f%%', explode=explode)
    centre_circle = plt.Circle((0, 0), 0.2, color='white', edgecolor='black', linewidth=0.8)
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    legend = ax.legend(wedges, labels, title="Nutrients", loc="center left", bbox_to_anchor=(0.9, 0.09))
    ax.axis('equal')
    ax.set_title('Nutritional Distribution (excluding Calories)')
    plt.savefig(donut_chart_path)
    plt.close()

    return a



# Example user input
# user_input = {'chicken': 20, 'Rice': 150}

# Calculate total nutrition based on user input
# total_nutrition = calculate_nutrition(user_input)

# Recommend a balanced diet based on total nutrition
# recommend_diet(total_nutrition)