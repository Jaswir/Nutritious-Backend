class Ingredient:
    def __init__(self, name, calories, cholesterol, dietary_fiber, phosphorus, potassium,
                 protein, saturated_fat, sodium, sugars, total_carbohydrate,
                 total_fat, serving_quantity, serving_unit, serving_weight_grams):
        self.name = name
        self.calories = calories
        self.cholesterol = cholesterol
        self.dietary_fiber = dietary_fiber
        self.phosphorus = phosphorus
        self.potassium = potassium
        self.protein = protein
        self.saturated_fat = saturated_fat
        self.sodium = sodium
        self.sugars = sugars
        self.total_carbohydrate = total_carbohydrate
        self.total_fat = total_fat
        self.serving_quantity = serving_quantity
        self.serving_unit = serving_unit
        self.serving_weight_grams = serving_weight_grams

    def __str__(self):
        return (f"Ingredient(calories={self.calories}, cholesterol={self.cholesterol}, "
                f"dietary_fiber={self.dietary_fiber}, phosphorus={self.phosphorus}, "
                f"potassium={self.potassium}, protein={self.protein}, "
                f"saturated_fat={self.saturated_fat}, sodium={self.sodium}, "
                f"sugars={self.sugars}, total_carbohydrate={self.total_carbohydrate}, "
                f"total_fat={self.total_fat}, serving_quantity={self.serving_quantity}, "
                f"serving_unit='{self.serving_unit}', serving_weight_grams={self.serving_weight_grams})")
