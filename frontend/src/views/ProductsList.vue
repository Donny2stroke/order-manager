<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2>
        <font-awesome-icon icon="tags" class="me-2" />
        Products
      </h2>
      <router-link to="/products/create" class="btn btn-primary">
        <font-awesome-icon icon="plus" class="me-1" />
        Create new product
      </router-link>
    </div>

    <h5>Active</h5>
    <table class="table table-striped table-hover align-middle">
      <thead>
        <tr>
          <th>Name</th>
          <th>Price</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in activeProducts" :key="product.id">
          <td>{{ product.name }}</td>
          <td>€{{ product.price }}</td>
          <td>
            <router-link
              :to="`/products/${product.id}`"
              class="btn btn-sm btn-outline-secondary me-2"
              title="Details"
            >
              <font-awesome-icon icon="eye" />
            </router-link>
            <router-link
              :to="`/products/${product.id}/edit`"
              class="btn btn-sm btn-outline-primary me-2"
              title="Modify"
            >
              <font-awesome-icon icon="pen" />
            </router-link>
            <button
              @click.prevent="deleteProduct(product.id)"
              class="btn btn-sm btn-outline-danger"
              title="Deactivate"
            >
              <font-awesome-icon icon="trash" />
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <h5 class="mt-5 text-muted">Deactivated</h5>
    <table class="table table-hover align-middle table-secondary">
      <thead>
        <tr class="text-muted">
          <th>Name</th>
          <th>Price</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in inactiveProducts" :key="product.id" class="text-muted">
          <td>{{ product.name }}</td>
          <td>€{{ product.price }}</td>
          <td>
            <router-link
              :to="`/products/${product.id}/edit`"
              class="btn btn-sm btn-outline-success"
              title="Modify / Reactivate"
            >
              <font-awesome-icon icon="pen" />
            </router-link>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../utils/api'

const products = ref([])

//Load all products from the backend API
const fetchProducts = async () => {
  const response = await api.get('/products/')
  products.value = response.data
}

/**
* Soft delete (deactivate) a product
* This sets is_active = false on backend
*/
const deleteProduct = async (id) => {
  if (confirm('Are you sure you want to deactivate this product?')) {
    try {
      await api.delete(`/products/${id}/`)

      const target = products.value.find(p => p.id === id)
      if (target) target.is_active = false

    } catch (err) {
      console.error('Error deactivating:', err)
    }
  }
}

//List of active products
const activeProducts = computed(() =>
  products.value.filter(p => p.is_active)
)
//List of deactivated (inactive) products
const inactiveProducts = computed(() =>
  products.value.filter(p => !p.is_active)
)

onMounted(fetchProducts)
</script>