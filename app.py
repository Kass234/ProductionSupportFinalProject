from flask import Flask, jsonify, request
from flask_cors import CORS
from models.recipe_model import RecipeModel
from models.rating_model import RatingModel

app = Flask(__name__)
CORS(app)


# gets all recipes
@app.route("/api/recipes")
def get_recipes():
    model = RecipeModel()
    data = model.get_all_recipes()
    return jsonify(data)

# gets a specific recipe
@app.route("/api/recipes/<int:recipe_id>")
def get_a_recipe(recipe_id):
    model = RecipeModel()
    data = model.get_recipe(recipe_id)
    return jsonify(data)

# creates a new recipe
@app.route("/api/recipes", methods=["POST"])
def create_recipe():
    data = request.get_json()
    user_id = data["user_id"]
    recipe_name = data["recipe_name"]
    description = data["description"]
    cooking_method = data["cooking_method"]
    ingredients = data["ingredients"]
    model = RecipeModel()
    recipe_data = model.create_recipe(user_id, recipe_name, description, cooking_method, ingredients)
    return jsonify(recipe_data), 201

# Deletes a recipe but only if the user created the original recipe
@app.route("/api/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    data = request.get_json()
    user_id = data["user_id"]
    model = RecipeModel()
    recipe_data = model.delete_recipe(recipe_id, user_id)
    return jsonify(recipe_data), 200

# shares the recipe
@app.route('/api/recipes/<int:recipe_id>/share')
def share_recipe(recipe_id):
    model = RecipeModel()
    data = model.share_recipe(recipe_id)
    return jsonify(data)

# adds a rating (updated - no user_id required)
@app.route('/api/recipes/<int:recipe_id>/rate', methods=['POST'])
def add_rating(recipe_id):
    data = request.get_json()
    score = data["score"]  # user_id removed from here
    
    # Optional: Add validation for score (e.g., 1-5)
    if not isinstance(score, int) or score < 1 or score > 5:
        return jsonify({"error": "Score must be an integer between 1 and 5"}), 400
    
    model = RatingModel()
    rating_data = model.add_rating(recipe_id, score)
    return jsonify(rating_data), 200

# Optional: Get all ratings for a recipe
@app.route('/api/recipes/<int:recipe_id>/ratings', methods=['GET'])
def get_recipe_ratings(recipe_id):
    model = RatingModel()
    ratings = model.get_recipe_ratings(recipe_id)
    return jsonify(ratings), 200

if __name__ == "__main__":
    app.run(debug=True)