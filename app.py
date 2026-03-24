from flask import Flask, jsonify, request
from flask_cors import CORS
from models.recipe_model import RecipeModel
from models.rating_model import RatingModel

app = Flask(__name__)
CORS(app)


#gets all recipes
@app.route("/api/recipes")
def get_recipes():
    model = RecipeModel()
    data = model.get_all_recipes()
    return jsonify(data)

#gets a sepcific recipe
@app.route("/api/recipes/<int:recipe_id>")
def get_a_recipe(recipe_id):
    model =RecipeModel()
    data =model.get_recipe(recipe_id)
    return jsonify(data)

#creates a new recipe
@app.route("/api/recipes",methods=["POST"])
def create_recipe():
    data = request.get_json()
    user_id=data["user_id"]
    recipe_name =data["recipe_name"]
    description = data["description"]
    cooking_method = data["cooking_method"]
    ingredients = data["ingredients"]
    model = RecipeModel()
    recipe_data =model.create_recipe(user_id,recipe_name,description,cooking_method,ingredients)
    return jsonify(recipe_data),201

#Delets a recipe but only if the the user created the original recipe
@app.route("/api/recipes/<int:recipe_id>",methods=["DELETE"])
def delete_recipe(recipe_id):
    data = request.get_json()
    user_id =data["user_id"]
    model = RecipeModel()
    recipe_data=model.delete_recipe(recipe_id,user_id)
    return jsonify(recipe_data),200


if __name__ == "__main__":
    app.run(debug=True)