<template>
  <div class="container py-5" v-if="order">
    <div class="row justify-content-center">
      <div class="col-lg-6">
        <div class="card shadow-sm">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">
              <font-awesome-icon icon="pen" class="me-2" />
              Edit Order
            </h2>

            <form @submit.prevent="updateOrder">
              <div class="mb-3">
                <label class="form-label">Customer name</label>
                <input
                  v-model="order.name"
                  type="text"
                  class="form-control"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Date</label>
                <input
                  v-model="order.date"
                  type="date"
                  class="form-control"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">description</label>
                <textarea
                  v-model="order.description"
                  class="form-control"
                  placeholder="Order details"
                ></textarea>
              </div>

              <h5 class="mb-3">Products:</h5>
              <div
                class="mb-3 d-flex justify-content-between align-items-center"
                v-for="prod in products"
                :key="prod.id"
              >
                <label class="form-label mb-0 w-75">
                  <font-awesome-icon icon="box" class="me-2 text-secondary" />
                  {{ prod.name }} - €{{ prod.price }}
                </label>
                <input
                  type="number"
                  min="0"
                  class="form-control w-25"
                  :value="getQuantity(prod.id)"
                  @input="updateQuantity(prod.id, $event.target.value)"
                />
              </div>

              <button type="submit" class="btn btn-primary w-100 mt-3">
                <font-awesome-icon icon="save" class="me-2" />
                Save changes
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>

  <p v-else class="text-center text-muted mt-5">Loading...</p>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../utils/api'

const route = useRoute()
const router = useRouter()

const order = ref(null)
const products = ref([])
const selectedProducts = ref([])

const getQuantity = (productId) => {
  const found = selectedProducts.value.find((p) => p.product_id === productId)
  return found ? found.quantity : 0
}

const updateQuantity = (productId, quantity) => {
  quantity = parseInt(quantity)
  selectedProducts.value = selectedProducts.value.filter(
    (p) => p.product_id !== productId
  )
  if (quantity > 0) {
    selectedProducts.value.push({ product_id: productId, quantity })
  }
}

const loadProducts = async () => {
  const { data } = await api.get('/products')
  products.value = data
}

onMounted(async () => {
  const { data } = await api.get(`/orders/${route.params.id}`)
  order.value = data

  selectedProducts.value = order.value.products.map((p) => ({
    product_id: p.product.id,
    quantity: p.quantity
  }))

  await loadProducts()
})

const updateOrder = async () => {
  try {
    await api.put(`/orders/${route.params.id}/`, {
      name: order.value.name,
      date: order.value.date,
      description: order.value.description,
      products_data: selectedProducts.value
    })
    router.push(`/orders/${route.params.id}`)
  } catch (err) {
    console.error("Error while updating:", err)
  }
}
</script>
