<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-5">
        <div class="card shadow-sm">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">
              <font-awesome-icon icon="plus" class="me-2" />
              New product
            </h2>

            <form @submit.prevent="createProduct">
              <div class="mb-3">
                <label class="form-label">Name</label>
                <input
                  v-model="name"
                  type="text"
                  class="form-control"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Price</label>
                <input
                  v-model="price"
                  type="number"
                  min="0.01"
                  step="0.01"
                  class="form-control"
                  required
                />
              </div>

              <button type="submit" class="btn btn-primary w-100">
                <font-awesome-icon icon="plus" class="me-1" />
                Create product
              </button>

              <div v-if="error" class="alert alert-danger mt-3 text-center">
                {{ error }}
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api'

const name = ref('')
const price = ref('')
const error = ref('')
const router = useRouter()

const createProduct = async () => {
  error.value = ''

  if (!name.value.trim()) {
    error.value = 'Product name is required.'
    return
  }

  const parsedPrice = parseFloat(price.value)
  if (isNaN(parsedPrice) || parsedPrice <= 0) {
    error.value = 'Price must be a number greater than 0.'
    return
  }

  try {
    await api.post('/products/', {
      name: name.value.trim(),
      price: parsedPrice
    })
    router.push('/products')
  } catch (err) {
    error.value = 'Error creating product.'
    console.error(err)
  }
}
</script>