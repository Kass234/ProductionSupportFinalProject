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

    def calculate_average(self,recipe_id):
        sql_average= "SELECT AVG(score) FROM ratings where recipe_id =%s"
        self.cursor.execute(sql_average,(recipe_id,))
        result =self.cursor.fetchone()
        average = result["AVG(score)"]
        sql_update ="UPDATE recipes SET average_rating = %s where recipe_id = %s"
        self.cursor.execute(sql_update,(average,recipe_id))
        self.conn.commit()
        return average


    def add_rating(self,user_id,recipe_id,score):
        created_at= datetime.now()
        sql= "SELECT * FROM ratings  where user_id =%s and recipe_id=%s"
        self.cursor.execute(sql,(user_id,recipe_id,))
        existing_rating =self.cursor.fetchone()
        if existing_rating is not None:
            sql_rating= "Update ratings SET score = %s where recipe_id =%s and user_id =%s"
            self.cursor.execute(sql_rating,(score,recipe_id,user_id,))
            self.conn.commit()
            self.calculate_average(recipe_id)
        else:
            sql_rating = "INSERT INTO ratings(recipe_id,user_id,score,created_at) VALUES(%s,%s,%s,%s)"
            self.cursor.execute(sql_rating,(recipe_id,user_id,score,created_at))
            self.conn.commit()
            self.calculate_average(recipe_id)
        return{
            "recipe_id":recipe_id,
            "user_id": user_id,
            "score":score,
            "created_at":created_at
        }
