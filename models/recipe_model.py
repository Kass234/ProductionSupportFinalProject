import mysql.connector
from config import DB_CONFIG
from datetime import datetime


class RecipeModel:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(dictionary=True)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def create_recipe(self, user_id, recipe_name, description, cooking_method, ingredients):
        average_rating = 0.0
        created_at = datetime.now()
        sql = "INSERT into recipes(user_id,recipe_name,description,cooking_method,average_rating,created_at) VALUES(%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql, (user_id, recipe_name, description, cooking_method, average_rating, created_at))
        self.conn.commit()
        rowid = self.cursor.lastrowid
        
        # Insert each ingredient as a simple text string
        for ingredient in ingredients:
            # Check if ingredient is a string or dict
            if isinstance(ingredient, dict):
                # If it's a dict, combine fields into a readable string
                ingredient_text = f"{ingredient.get('name', '')} - {ingredient.get('quantity', '')} {ingredient.get('unit', '')} ({ingredient.get('notes', '')})".strip()
                # Clean up empty parentheses
                ingredient_text = ingredient_text.replace('()', '').strip(' -')
            else:
                # If it's already a string, use it directly
                ingredient_text = ingredient
            
            sql_for_ingredient = "INSERT into ingredients(recipe_id, ingredient_text) VALUES(%s, %s)"
            self.cursor.execute(sql_for_ingredient, (rowid, ingredient_text))
        
        self.conn.commit()
        
        # Format ingredients for response
        formatted_ingredients = []
        for ingredient in ingredients:
            if isinstance(ingredient, dict):
                formatted_ingredients.append(f"{ingredient.get('name', '')} - {ingredient.get('quantity', '')} {ingredient.get('unit', '')} ({ingredient.get('notes', '')})".strip().replace('()', '').strip(' -'))
            else:
                formatted_ingredients.append(ingredient)
        
        return {
            "recipe_id": rowid,
            "user_id": user_id,
            "name": recipe_name,
            "description": description,
            "cooking_method": cooking_method,
            "average_rating": average_rating,
            "created_at": created_at,
            "ingredients": formatted_ingredients
        }
    
    def get_all_recipes(self):
        sql = "SELECT * FROM recipes"
        self.cursor.execute(sql)
        all_recipes = self.cursor.fetchall()
        
        for recipe in all_recipes:
            sql1 = "SELECT ingredient_text FROM ingredients where recipe_id = %s"
            self.cursor.execute(sql1, (recipe['recipe_id'],))
            ingredients = self.cursor.fetchall()
            # Extract just the text from each ingredient
            recipe["ingredients"] = [ingredient['ingredient_text'] for ingredient in ingredients]
        
        return all_recipes
    
    def get_recipe(self, recipe_id):
        sql = "SELECT * from recipes where recipe_id = %s"
        self.cursor.execute(sql, (recipe_id,))
        recipe_found = self.cursor.fetchone()
        
        if recipe_found:
            sql1 = "SELECT ingredient_text FROM ingredients where recipe_id = %s"
            self.cursor.execute(sql1, (recipe_found["recipe_id"],))
            ingredients = self.cursor.fetchall()
            # Extract just the text from each ingredient
            recipe_found["ingredients"] = [ingredient['ingredient_text'] for ingredient in ingredients]
        
        return recipe_found
    
    def delete_recipe(self, recipe_id, user_id):
        sql = "SELECT * from recipes where recipe_id = %s"
        self.cursor.execute(sql, (recipe_id,))
        recipe_found = self.cursor.fetchone()
        
        if recipe_found and recipe_found["user_id"] == user_id:
            sql1 = "DELETE from recipes where recipe_id = %s"
            self.cursor.execute(sql1, (recipe_id,))
            self.conn.commit()
            return {"message": "Recipe successfully deleted"}
        else:
            return {"error": "Unauthorized - you can only delete your own recipe"}
    
    def share_recipe(self, recipe_id):
        recipe = self.get_recipe(recipe_id)
        return recipe