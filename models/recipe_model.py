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
        
        formatted_ingredients = []
        
        # Check if ingredients is a list or a string
        if isinstance(ingredients, str):
            # If it's a string, treat it as a single ingredient
            ingredients_list = [ingredients]
        elif isinstance(ingredients, list):
            # If it's already a list, use it directly
            ingredients_list = ingredients
        else:
            # Default to empty list
            ingredients_list = []
        
        # Insert each ingredient
        for ingredient in ingredients_list:
            # Handle different input formats
            if isinstance(ingredient, dict):
                # Format detailed ingredient
                parts = []
                if ingredient.get('quantity'):
                    parts.append(ingredient['quantity'])
                if ingredient.get('unit'):
                    parts.append(ingredient['unit'])
                if ingredient.get('name'):
                    parts.append(ingredient['name'])
                if ingredient.get('notes'):
                    parts.append(f"({ingredient['notes']})")
                ingredient_text = ' '.join(parts).strip()
                # Clean up empty parentheses
                ingredient_text = ingredient_text.replace('()', '').strip(' -')
            else:
                # Simple string ingredient
                ingredient_text = str(ingredient).strip()
            
            # Only insert if not empty
            if ingredient_text:
                sql_for_ingredient = "INSERT into ingredients(recipe_id, ingredient_text) VALUES(%s, %s)"
                self.cursor.execute(sql_for_ingredient, (rowid, ingredient_text))
                formatted_ingredients.append(ingredient_text)
        
        self.conn.commit()
        
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
            recipe_found["ingredients"] = [ingredient['ingredient_text'] for ingredient in ingredients]
        
        return recipe_found
    
    def update_recipe(self, recipe_id, user_id, recipe_name=None, description=None, cooking_method=None, ingredients=None):
        """
        Update an existing recipe. Only the recipe owner can update it.
        Parameters that are None will not be updated.
        """
        # First, check if the recipe exists and belongs to the user
        sql_check = "SELECT * FROM recipes WHERE recipe_id = %s"
        self.cursor.execute(sql_check, (recipe_id,))
        recipe_found = self.cursor.fetchone()
        
        if not recipe_found:
            return {"error": "Recipe not found"}
        
        if recipe_found["user_id"] != user_id:
            return {"error": "Unauthorized - you can only edit your own recipe"}
        
        # Build dynamic update query based on what fields are provided
        update_fields = []
        update_values = []
        
        if recipe_name is not None:
            update_fields.append("recipe_name = %s")
            update_values.append(recipe_name)
        
        if description is not None:
            update_fields.append("description = %s")
            update_values.append(description)
        
        if cooking_method is not None:
            update_fields.append("cooking_method = %s")
            update_values.append(cooking_method)
        
        # If no fields to update (except ingredients), skip recipes table update
        if update_fields:
            sql_update = f"UPDATE recipes SET {', '.join(update_fields)} WHERE recipe_id = %s"
            update_values.append(recipe_id)
            self.cursor.execute(sql_update, update_values)
            self.conn.commit()
        
        # Update ingredients if provided
        if ingredients is not None:
            # First, delete all existing ingredients for this recipe
            sql_delete_ingredients = "DELETE FROM ingredients WHERE recipe_id = %s"
            self.cursor.execute(sql_delete_ingredients, (recipe_id,))
            
            # Prepare ingredients list
            if isinstance(ingredients, str):
                # If it's a string, treat it as a single ingredient
                ingredients_list = [ingredients]
            elif isinstance(ingredients, list):
                # If it's already a list, use it directly
                ingredients_list = ingredients
            else:
                # Default to empty list
                ingredients_list = []
            
            # Then insert the new ingredients
            formatted_ingredients = []
            for ingredient in ingredients_list:
                # Handle different input formats
                if isinstance(ingredient, dict):
                    # Format detailed ingredient
                    parts = []
                    if ingredient.get('quantity'):
                        parts.append(ingredient['quantity'])
                    if ingredient.get('unit'):
                        parts.append(ingredient['unit'])
                    if ingredient.get('name'):
                        parts.append(ingredient['name'])
                    if ingredient.get('notes'):
                        parts.append(f"({ingredient['notes']})")
                    ingredient_text = ' '.join(parts).strip()
                    # Clean up empty parentheses
                    ingredient_text = ingredient_text.replace('()', '').strip(' -')
                else:
                    # Simple string ingredient
                    ingredient_text = str(ingredient).strip()
                
                # Only insert if not empty
                if ingredient_text:
                    sql_insert_ingredient = "INSERT INTO ingredients(recipe_id, ingredient_text) VALUES(%s, %s)"
                    self.cursor.execute(sql_insert_ingredient, (recipe_id, ingredient_text))
                    formatted_ingredients.append(ingredient_text)
            
            self.conn.commit()
        
        # Get the updated recipe
        return self.get_recipe(recipe_id)
    
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