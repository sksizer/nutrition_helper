import json

from colorama import Fore, Style
from tabulate import tabulate

from ingredient_database import IngredientDatabase

def calculate_total_nutrition(food_dict):
    db = IngredientDatabase('./data')
    total_nutrition = {}

    for food_item, amount in food_dict.items():
        ingredient = db.get_by_name(food_item, amount)
        if ingredient is None:
            raise ValueError(f"Ingredient not found: {food_item}")
        
        for nutrient, value in ingredient['scaled_values'].items():
            if nutrient in total_nutrition:
                total_nutrition[nutrient][0] += value[0]
            else:
                total_nutrition[nutrient] = value.copy()

    return {
        'total_nutrition': total_nutrition
    }


def print_nutrition_table(nutrition_data, macro_color=Fore.GREEN, micro_color=Fore.CYAN):
    # Define macronutrients and micronutrients for categorization
    macronutrients = ['calories', 'protein', 'total_fat', 'saturated_fat', 'cholesterol', 'sodium', 'carbohydrates', 'fiber', 'sugars']
    micronutrients = ['potassium', 'calcium', 'iron', 'magnesium', 'phosphorus', 'vitamin_A', 'vitamin_C', 'thiamin', 'riboflavin', 'niacin', 'vitamin_B6', 'folate', 'vitamin_K']

    # Prepare table data
    table_data = []
    headers = ["Nutrient", "Amount", "Unit"]

    # Add macronutrients
    table_data.append([macro_color + "Macronutrients" + Style.RESET_ALL, "", ""])
    for nutrient, values in nutrition_data['total_nutrition'].items():
        if nutrient in macronutrients:
            table_data.append([macro_color + nutrient + Style.RESET_ALL, values[0], values[1]])

    # Add micronutrients
    table_data.append([micro_color + "Micronutrients" + Style.RESET_ALL, "", ""])
    for nutrient, values in nutrition_data['total_nutrition'].items():
        if nutrient in micronutrients:
            table_data.append([micro_color + nutrient + Style.RESET_ALL, values[0], values[1]])

    # Print table
    print(tabulate(table_data, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    try:
        # Load food_dict from example.json
        with open('example.json', 'r') as file:
            food_dict = json.load(file)
        nutrition_summary = calculate_total_nutrition(food_dict)
        print_nutrition_table(nutrition_summary)
    except ValueError as e:
        print(e)