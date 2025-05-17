<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-body" :class="{ 'text-muted': !product.is_active }">
            <h2 class="card-title text-center mb-4">
              <font-awesome-icon icon="tag" class="me-2" />
              Product details
            </h2>

            <p class="mb-3">
              <strong>Name:</strong>
              <span class="ms-1">{{ product.name }}</span>
            </p>

            <p class="mb-3">
              <strong>Price:</strong>
              <font-awesome-icon icon="euro-sign" class="ms-2 me-1 text-muted" />
              {{ product.price }}
            </p>

            <p class="mb-4">
              <strong>Status:</strong>
              <span class="ms-1">
                <span
                  class="badge"
                  :class="product.is_active ? 'bg-success' : 'bg-secondary'"
                >
                  {{ product.is_active ? 'Active' : 'Deactivated' }}
                </span>
              </span>
            </p>

            <router-link
              :to="`/products/${product.id}/edit`"
              class="btn btn-outline-primary w-100"
            >
              <font-awesome-icon icon="pen" class="me-1" />
              Modify
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../utils/api'

const route = useRoute()
const product = ref({})

const fetchProduct = async () => {
  const response = await api.get(`/products/${route.params.id}/`)
  product.value = response.data
}

onMounted(fetchProduct)
</script>