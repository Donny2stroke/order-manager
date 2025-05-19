<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2>
        <font-awesome-icon icon="box" class="me-2" />
        Orders
      </h2>
      <router-link to="/orders/new" class="btn btn-primary">
        <font-awesome-icon icon="plus" class="me-1" />
        Create new order
      </router-link>
    </div>

    <form class="row g-3 align-items-end mb-4" @submit.prevent="fetchOrders">
      <div class="col-md-5">
        <label class="form-label">Search by name or description</label>
        <input v-model="search" type="text" class="form-control" placeholder="Es. Mario Rossi / Order on commission" />
      </div>
      <div class="col-md-3">
        <label class="form-label">Date</label>
        <input v-model="date" type="date" class="form-control" />
      </div>
      <div class="col-md-2">
        <button type="submit" class="btn btn-primary w-100">
          <font-awesome-icon icon="search" class="me-1" />
          Search
        </button>
      </div>
    </form>

    <div v-if="orders.length">
      <table class="table table-striped table-hover align-middle">
        <thead>
          <tr>
            <th>Customer</th>
            <th>Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orders" :key="order.id">
            <td>
              <router-link :to="`/orders/${order.id}`" class="fw-semibold text-decoration-none">
                {{ order.name }}
              </router-link>
            </td>
            <td>{{ new Date(order.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }) }}</td>
            <td>
              <router-link :to="`/orders/${order.id}/edit`" class="btn btn-sm btn-outline-primary me-2" title="Modify">
                <font-awesome-icon icon="pen" />
              </router-link>
              <button @click="deleteOrder(order.id)" class="btn btn-sm btn-outline-danger" title="Delete">
                <font-awesome-icon icon="trash" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-else class="text-muted">No orders found.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../utils/api'

const orders = ref([])
const search = ref('')
const date = ref('')

/**
* Fetches the list of orders from the API, applying filters if set.
* Results are sorted by date (most recent first).
*/
const fetchOrders = async () => {
  try {
    const params = {}
    if (search.value) params.search = search.value
    if (date.value) params.date = date.value

    const token = localStorage.getItem('token')
    const { data } = await api.get(import.meta.env.VITE_API_URL + '/orders', {
      headers: { Authorization: `Bearer ${token}` },
      params
    })

    //orders.value = data
    
    // Sort orders by date descending
    orders.value = data.sort((a, b) => new Date(b.date) - new Date(a.date))


  } catch (error) {
    console.error('Error retrieving orders:', error)
  }
}

//Deletes an order after confirmation and updates the list.
const deleteOrder = async (id) => {
  const confirmed = confirm('Are you sure you want to delete this order?')
  if (!confirmed) return

  try {
    await api.delete(`/orders/${id}/`)
    // Remove order from local list
    orders.value = orders.value.filter(o => o.id !== id)
  } catch (err) {
    console.error("Error while deleting:", err)
  }
}

// Load orders when component mounts
onMounted(fetchOrders)
</script>
