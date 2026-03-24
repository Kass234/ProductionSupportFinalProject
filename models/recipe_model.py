import mysql.connector
from config import DB_CONFIG
from datetime import  datetime


class RecipeModel:
    def __init__(self):
        self.conn = mysql.connector.connect(DB_CONFIG)
        self.cursor = self.conn.cursor(dictionary=True)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def create_recipe(self,user_id,recipe_name,description,cooking_method,ingredients):
        average_rating = 0.0
        created_at = datetime.now()
        sql = "INSERT into recipes(user_id,recipe_name,description,cooking_method,average_rating,created_at) VALUES(%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(sql,(user_id,recipe_name,description,cooking_method,average_rating,created_at))
        self.conn.commit()
        rowid = self.cursor.lastrowid
        for ingredient in ingredients:
            sql_for_ingredient = "INSERT into ingredients(recipe_id,name,category,quantity,unit,notes) VALUES(%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(sql_for_ingredient,(rowid,ingredient["name"],ingredient["category"],ingredient["quantity"],ingredient["unit"],ingredient["notes"]))
        self.conn.commit()
        return {
            "recipe_id":rowid,
            "user_id": user_id,
            "name": recipe_name,
            "description": description,
            "cooking_method":cooking_method,
            "average_rating":average_rating,
            "created_at":created_at,
            "ingredients":ingredients
        }
    def get_all_recipes(self):
        sql = "SELECT * FROM recipes "
        self.cursor.execute(sql)
        all_recipes=self.cursor.fetchall()
        for recipes in all_recipes:
            sql1 = "SELECT * from ingredients where recipe_id = %s"
            self.cursor.execute(sql1,(recipes['recipe_id'],))
            ingredients =self.cursor.fetchall()
            recipes["ingredients"] = ingredients
        return all_recipes
    
    def get_recipe(self,recipe_id):
        sql = "SELECT * from recipes where recipe_id = %s"
        self.cursor.execute(sql,(recipe_id,))
        recipe_found =self.cursor.fetchone()
        sql1 = "SELECT * from ingredients where recipe_id = %s"
        self.cursor.execute(sql1,(recipe_found["recipe_id"],))
        ingredients =self.cursor.fetchall()
        recipe_found["ingredients"] = ingredients
        return recipe_found
    
    def delete_recipe(self,recipe_id,user_id):
        sql = "SELECT * from recipes where recipe_id = %s"
        self.cursor.execute(sql,(recipe_id,))
        recipe_found =self.cursor.fetchone()
        if recipe_found["user_id"]== user_id:
            sql1 = "Delete from recipes where recipe_id = %s"
            self.cursor.execute(sql1,(recipe_id,))
            self.conn.commit()
            return{"message":"Recipe succesfully deleted"}
        else:
            return{"error": "Unauthorized- you can only delete your own recipe"}
    
    def share_recipe(self,recipe_id):
        recipe = self.get_recipe(recipe_id)
        return recipe

        
