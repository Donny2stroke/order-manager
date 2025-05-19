<template>
  <div class="container py-5" v-if="order">
    <div class="card shadow-sm">
      <div class="card-body">
        <h2 class="card-title text-center mb-4">
          <font-awesome-icon icon="file-alt" class="me-2" />
          Order Detail
        </h2>

        <h4 class="mb-3">{{ order.name }}</h4>

        <p class="mb-2">
          <font-awesome-icon icon="calendar" class="me-2 text-muted" />
          <strong>Date:</strong> {{ order.date }}
        </p>

        <p class="mb-4">
          <font-awesome-icon icon="info-circle" class="me-2 text-muted" />
          <strong>Description:</strong> {{ order.description }}
        </p>

        <h5 class="mb-3">Products:</h5>
        <ul class="list-group">
          <li
            v-for="p in order.products"
            :key="p.product.id"
            class="list-group-item d-flex justify-content-between align-items-center"
          >
            <span>
              <font-awesome-icon icon="box" class="me-2 text-secondary" />
              {{ p.product.name }}
            </span>
            <span v-if="!p.product.is_active" class="badge bg-secondary ms-2">Deactivated</span>
            <span>
              {{ p.quantity }} x €{{ p.product.price }}
            </span>
          </li>
        </ul>
      </div>
    </div>
  </div>

  <p v-else class="text-center text-muted mt-5">Loading...</p>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import api from '../utils/api'

const route = useRoute()
const order = ref(null)

//Fetches the order details from the API using the order ID in the route.
const fetchOrder = async () => {
  try {
    const { data } = await api.get(`/orders/${route.params.id}`)
    order.value = data
  } catch (err) {
    console.error('Error loading order:', err)
  }
}

onMounted(fetchOrder)
</script>
