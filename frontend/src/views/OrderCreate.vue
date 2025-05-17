<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-6">
        <div class="card shadow-sm">
          <div class="card-body">
            <h2 class="card-title mb-4 text-center">
              <font-awesome-icon icon="plus" class="me-2" />
              New Order
            </h2>

            <form @submit.prevent="createOrder">
              <div class="mb-3">
                <label class="form-label">Customer name</label>
                <input
                  v-model="name"
                  type="text"
                  class="form-control"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Date</label>
                <input
                  v-model="date"
                  type="date"
                  class="form-control"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea
                  v-model="description"
                  class="form-control"
                  placeholder="Order details"
                ></textarea>
              </div>

              <h5 class="mt-4 mb-2">Products</h5>
              <div
                class="mb-3 d-flex justify-content-between align-items-center"
                v-for="prod in products"
                :key="prod.id"
              >
                <label class="form-label mb-0 w-75">
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

              <button type="submit" class="btn btn-primary w-100 mt-4">
                <font-awesome-icon icon="plus" class="me-2" />
                Create order
              </button>

              <div v-if="formError" class="alert alert-danger mt-3 text-center">
                {{ formError }}
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
import { useRouter } from 'vue-router'
import api from '../utils/api'

const name = ref('')
const date = ref('')
const description = ref('')
const products = ref([])
const selectedProducts = ref([])
const formError = ref('')
const router = useRouter()

const loadProducts = async () => {
  const { data } = await api.get('/products')
  products.value = data
}

onMounted(loadProducts)

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

const createOrder = async () => {
  formError.value = ''
  if (selectedProducts.value.length === 0) {
    formError.value = 'Devi selezionare almeno un prodotto con quantità.'
    return
  }

  try {
    await api.post('/orders/', {
      name: name.value,
      date: date.value,
      description: description.value,
      products_data: selectedProducts.value
    })
    router.push('/orders')
  } catch (err) {
    console.error('Errore nella creazione:', err)
    formError.value = 'Errore durante la creazione. Riprova.'
  }
}
</script>
