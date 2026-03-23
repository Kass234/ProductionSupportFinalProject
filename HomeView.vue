<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

const recipes = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const response = await axios.get("http://localhost:5000/api/recipes")
    recipes.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
})
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
</style>

<template>
  <div class="home">
    <h1>Recipes</h1>

    <div v-if="loading">Loading...</div>

    <div v-else>
      <div v-for="recipe in recipes" :key="recipe.id" class="card">
        <h2>{{ recipe.recipe_name }}</h2>
        <p>{{ recipe.recipe_id }}</p>
        <p>{{ recipe.user_id }}</p>
        <p>{{ recipe.cooking_method }}</p>
        <p>{{ recipe.average_rating }}</p>
        <p>{{ recipe.created_at }}</p>
      </div>
    </div>
  </div>
</template>