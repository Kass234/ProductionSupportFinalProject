import mysql.connector
from config import DB_CONFIG


class RecipeModel:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(dictionary=True)

    def __del__(self):
        self.cursor.close()
        self.conn.close()
    
    def get_all_recipes(self):
        self.cursor.execute("SELECT * FROM recipes")
        return self.cursor.fetchall()

    def test(self):
        self.cursor.execute("SELECT 1")
        result = self.cursor.fetchone()
        return result