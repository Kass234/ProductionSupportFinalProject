import mysql.connector
from config import DB_CONFIG
import datetime

class RatingModel:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(dictionary=True)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def calculate_average(self, recipe_id):
        sql_average = "SELECT AVG(score) FROM ratings where recipe_id = %s"
        self.cursor.execute(sql_average, (recipe_id,))
        result = self.cursor.fetchone()
        average = result["AVG(score)"] if result["AVG(score)"] is not None else 0.0
        
        # Round to 1 decimal place
        average = round(average, 1)
        
        sql_update = "UPDATE recipes SET average_rating = %s where recipe_id = %s"
        self.cursor.execute(sql_update, (average, recipe_id))
        self.conn.commit()
        return average

    def add_rating(self, recipe_id, score):
        created_at = datetime.datetime.now()
        
        # Insert new rating (no user_id check anymore)
        sql_rating = "INSERT INTO ratings(recipe_id, score, created_at) VALUES(%s, %s, %s)"
        self.cursor.execute(sql_rating, (recipe_id, score, created_at))
        self.conn.commit()
        
        # Update the average rating
        self.calculate_average(recipe_id)
        
        return {
            "recipe_id": recipe_id,
            "score": score,
            "created_at": created_at
        }
    
    def get_recipe_ratings(self, recipe_id):
        """Optional: Get all ratings for a recipe"""
        sql = "SELECT * FROM ratings WHERE recipe_id = %s ORDER BY created_at DESC"
        self.cursor.execute(sql, (recipe_id,))
        return self.cursor.fetchall()