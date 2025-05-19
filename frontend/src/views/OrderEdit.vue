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
                <label class="form-label mb-0 w-75 d-flex justify-content-between align-items-center">
                  <div>
                    <font-awesome-icon icon="box" class="me-2 text-secondary" />
                    {{ prod.name }} - €{{ prod.price }}
                  </div>
                  <span v-if="!prod.is_active" class="badge bg-secondary">Deactivated</span>
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

//Retrieves the quantity of a given product in the order.
const getQuantity = (productId) => {
  const found = selectedProducts.value.find((p) => p.product_id === productId)
  return found ? found.quantity : 0
}

//Updates or adds the quantity for a specific product. Removes entries with zero quantity.
const updateQuantity = (productId, quantity) => {
  quantity = parseInt(quantity)
  selectedProducts.value = selectedProducts.value.filter(
    (p) => p.product_id !== productId
  )
  if (quantity > 0) {
    selectedProducts.value.push({ product_id: productId, quantity })
  }
}

// Loads products and merges active + selected inactive
const loadProducts = async () => {
  const { data: allProducts } = await api.get('/products')

  // Products selected in the order (could be inactive)
  const selectedIds = selectedProducts.value.map(p => p.product_id)
  const selectedProductsInfo = allProducts.filter(p => selectedIds.includes(p.id))

  // Active products not already selected
  const activeNotSelected = allProducts.filter(p => p.is_active && !selectedIds.includes(p.id))

  // Merge selected (even if inactive) with active products not already in the order
  products.value = [...selectedProductsInfo, ...activeNotSelected]
}

// On component mount: fetch the order details and product list
onMounted(async () => {
  const { data } = await api.get(`/orders/${route.params.id}`)
  order.value = data

  // Map the products into the selectedProducts structure
  selectedProducts.value = order.value.products.map((p) => ({
    product_id: p.product.id,
    quantity: p.quantity
  }))

  await loadProducts()
})

//Submits the updated order to the API.
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
