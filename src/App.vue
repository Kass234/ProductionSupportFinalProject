<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

const showForm = ref(false)
const recipes = ref([])
const isEditing = ref(false)
const editingId = ref(null)
const loading = ref(true)
const newRecipe = ref({
  recipe_name: "",
  description: "",
  cooking_method: "",
  ingredients: ""
})
const editRecipe = (recipe) => {
  newRecipe.value = {
    recipe_name: recipe.recipe_name,
    description: recipe.description,
    cooking_method: recipe.cooking_method,
    ingredients: recipe.ingredients
  }
  // will edit instead of adding a new one
  editingId.value = recipe.recipe_id
  isEditing.value = true
  showForm.value = true
}
const rateRecipe = async (recipeId, event) => {
  const score = Number(event.target.value)

  try {
    await axios.post(
      `http://localhost:5000/api/recipes/${recipeId}/rate`,
      {
        score: score   
      }
    )
  } catch (error) {
    console.error("Rating failed:", error.response?.data || error.message)
  }
}
onMounted(async () => {            //default get all
  try {
    const response = await axios.get("http://localhost:5000/api/recipes")
    recipes.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
})

const submitRecipe = async () => {
  try {
    if (isEditing.value) {
      //  edit
      await axios.put(
        `http://localhost:5000/api/recipes/${editingId.value}`,
        {
          ...newRecipe.value,
          user_id: 1
        }
      )
    } else {
      //  add
      await axios.post(
        "http://localhost:5000/api/recipes",
        {
          ...newRecipe.value,
          user_id: 1
        }
      )
    }
    // reset form
    newRecipe.value = {
      recipe_name: "",
      description: "",
      cooking_method: "",
      ingredients: ""
    }
   // stops editing state
    showForm.value = false
    isEditing.value = false
    editingId.value = null

  } catch (error) {
    console.error(error)
  }
}

const deleteRecipe = async (id) => {
  try {
    await axios.delete(`http://localhost:5000/api/recipes/${id}`, {
      data: {
        user_id: 1  //replace with way to get real user_id
      }
    })
      
  } catch (error) {
    console.error(error)
  }
}

</script>

<style scoped>
.home {
  padding: 20px;
}

.card {
  border: 1px solid #ccc;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 8px;
}
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);

  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: rgb(14, 2, 2);
  padding: 20px;
  border-radius: 8px;
  width: 300px;
}

.modal-content input {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
}

.actions {
  display: flex;
  justify-content: space-between;
}
</style>

<template>
  <div class="home">
    <h1>List of Recipes</h1>
    
    <button @click="showForm = true">Add New Recipe</button>
      <div v-if="showForm" class="modal">
  <div class="modal-content">
    <h2>Add Recipe</h2>

    <input v-model="newRecipe.recipe_name" placeholder="Recipe Name" />
    <input v-model="newRecipe.description" placeholder="Description" />
    <input v-model="newRecipe.cooking_method" placeholder="Cooking Method" />
    <input v-model="newRecipe.ingredients" placeholder="Ingredients" />

    <div class="actions">
      <button @click="submitRecipe">Submit</button>
      <button @click="showForm = false">Cancel</button>
    </div>
  </div>
</div>
    <div v-if="loading">Loading...</div>

    <table v-else border="1" cellspacing="0" cellpadding="8">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Description</th>
          <th>ingredients</th>
          <th>User</th> 
          <th>Method</th>
          <th>Rating</th>
          <th>Created</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="recipe in recipes" :key="recipe.recipe_id">
          <td>{{ recipe.recipe_id }}</td>
          <td>{{ recipe.recipe_name }}</td>
          <td>{{ recipe.description }}</td>
          <td>{{ recipe.ingredients }}</td>
          <td>{{ recipe.user_id }}</td>     
          <td>{{ recipe.cooking_method }}</td>
          <td>
  <select @change="rateRecipe(recipe.recipe_id, $event)">
    <option disabled selected>Rate</option>
    <option v-for="n in 5" :key="n" :value="n">
      {{ n }}
    </option>
  </select>

  <div>⭐ {{ recipe.average_rating }}</div>
</td>
          <td>{{ recipe.created_at }}</td>
           <td>
            <button @click="editRecipe(recipe)">Edit</button>
            <button @click="deleteRecipe(recipe.recipe_id)">Delete</button>
          </td>
        </tr>

        <tr v-if="recipes.length === 0">
          <td colspan="6">No recipes found try adding one</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>