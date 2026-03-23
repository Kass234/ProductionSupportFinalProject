from flask import Flask, jsonify
from flask_cors import CORS
from model import RecipeModel

app = Flask(__name__)
CORS(app)

@app.route("/api/test")
def test():
    model = RecipeModel()
    result = model.test()
    return jsonify({"message": "Flask and MySQL are connected!", "result": result})

@app.route("/api/recipes")
def get_recipes():
    model = RecipeModel()
    data = model.get_all_recipes()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)