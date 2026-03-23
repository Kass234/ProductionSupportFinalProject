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
            