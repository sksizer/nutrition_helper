import os
import json

class IngredientDatabase:
    def __init__(self, directory):
        self.directory = directory
        self.by_short_name = {}
        self.by_name = {}
        self.by_usda_food_code = {}
        self.by_fdc_id = {}
        self.load_ingredients()

    def load_ingredients(self):
        for filename in os.listdir(self.directory):
            if filename.endswith('.json'):
                filepath = os.path.join(self.directory, filename)
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    self.index_ingredient(data)

    def index_ingredient(self, ingredient):
        # Index the ingredient in separate dictionaries
        if 'short_name' in ingredient:
            self.by_short_name[ingredient['short_name']] = ingredient
        if 'name' in ingredient:
            self.by_name[ingredient['name']] = ingredient
        if 'USDA_Food_Code' in ingredient:
            self.by_usda_food_code[ingredient['USDA_Food_Code']] = ingredient
        if 'FDC_ID' in ingredient:
            self.by_fdc_id[ingredient['FDC_ID']] = ingredient

    def get_by_short_name(self, short_name, amount=None):
        ingredient = self.by_short_name.get(short_name)
        return self.scale_nutrients(ingredient, amount or ingredient['serving_size'][0])

    def get_by_name(self, name, amount=None):
        ingredient = self.by_name.get(name)
        return self.scale_nutrients(ingredient, amount or ingredient['serving_size'][0])

    def get_by_usda_food_code(self, usda_food_code, amount=None):
        ingredient = self.by_usda_food_code.get(usda_food_code)
        return self.scale_nutrients(ingredient, amount or ingredient['serving_size'][0])

    def get_by_fdc_id(self, fdc_id, amount=None):
        ingredient = self.by_fdc_id.get(fdc_id)
        return self.scale_nutrients(ingredient, amount or ingredient['serving_size'][0])

    def scale_nutrients(self, ingredient, amount):
        if ingredient is None:
            return None
        scaled_values = {}
        base_amount = ingredient['serving_size'][0]
        for key, value in ingredient['values'].items():
            scaled_values[key] = [(value[0] * amount) / base_amount, value[1]]
        return {
            'name': ingredient['name'],
            'scaled_values': scaled_values
        }

# # Usage example
# db = IngredientDatabase('./data')
# scaled_ingredient = db.get_by_name('Carrots, raw', 200)  # Get nutritional values for 200 grams
# # print(scaled_ingredient)
