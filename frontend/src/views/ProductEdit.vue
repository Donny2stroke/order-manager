<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-5">
        <div class="card shadow-sm">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">
              <font-awesome-icon icon="pen" class="me-2" />
              Modify product
            </h2>

            <form @submit.prevent="updateProduct">
              <div class="mb-3">
                <label class="form-label">Name</label>
                <input
                  v-model="product.name"
                  type="text"
                  class="form-control"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Price</label>
                <input
                  v-model="product.price"
                  type="number"
                  class="form-control"
                  step="0.01"
                  min="0.01"
                  required
                />
              </div>

              <div class="form-check form-switch mb-3">
                <input
                  v-model="product.is_active"
                  class="form-check-input"
                  type="checkbox"
                  id="isActiveSwitch"
                />
                <label class="form-check-label" for="isActiveSwitch">
                  Active
                </label>
              </div>

              <button type="submit" class="btn btn-primary w-100">
                <font-awesome-icon icon="save" class="me-2" />
                Save
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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../utils/api'

const route = useRoute()
const router = useRouter()
const product = ref({})
const error = ref('')

const fetchProduct = async () => {
  const response = await api.get(`/products/${route.params.id}/`)
  product.value = response.data
}

const updateProduct = async () => {
  error.value = ''

  if (!product.value.name || !product.value.name.trim()) {
    error.value = 'Product name is required.'
    return
  }

  const parsedPrice = parseFloat(product.value.price)
  if (isNaN(parsedPrice) || parsedPrice <= 0) {
    error.value = 'Price must be a number greater than 0.'
    return
  }

  try {
    await api.put(`/products/${route.params.id}/`, {
      name: product.value.name.trim(),
      price: parsedPrice,
      is_active: product.value.is_active 
    })
    router.push(`/products/${route.params.id}`)
  } catch (err) {
    error.value = 'Error saving changes.'
    console.error(err)
  }
}

onMounted(fetchProduct)
</script>
