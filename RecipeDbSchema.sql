CREATE DATABASE recipedb;
USE recipedb;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE recipes (
    recipe_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    recipe_name VARCHAR(100) NOT NULL,
    description TEXT,
    cooking_method TEXT,
    average_rating FLOAT DEFAULT 0.0,
    created_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE ingredients (
    ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_id INT,
    name VARCHAR(100) NOT NULL,
    category ENUM(
        'protein',
        'vegetable',
        'fruit',
        'grain',
        'dairy',
        'seasoning',
        'herb',
        'sauce',
        'liquid',
        'other'
    ) DEFAULT NULL,
    quantity VARCHAR(50) DEFAULT NULL,
    unit VARCHAR(20) DEFAULT NULL,
    notes VARCHAR(200) DEFAULT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE
);

CREATE TABLE ratings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_id INT,
    score INT NOT NULL,
    created_at DATETIME,
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE
);