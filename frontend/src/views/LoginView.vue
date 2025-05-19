<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-4">
        <div class="card shadow-sm">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">
              <font-awesome-icon icon="sign-in-alt" class="me-2" />
              Login
            </h2>
            <form @submit.prevent="handleLogin">
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input
                  v-model="username"
                  type="text"
                  id="username"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input
                  v-model="password"
                  type="password"
                  id="password"
                  class="form-control"
                  required
                />
              </div>
              <button type="submit" class="btn btn-primary w-100">
                Login
              </button>
              <p v-if="error" class="text-danger mt-3 text-center">
                {{ error }}
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../utils/api'
import { useRouter } from 'vue-router'
import { login } from '../stores/auth'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

// Function that handles login submission
const handleLogin = async () => {
  try {
    // Send credentials to obtain JWT tokens
    const { data } = await api.post(import.meta.env.VITE_API_URL + '/token/', {
      username: username.value,
      password: password.value
    })
    // Save credentials to store (localStorage)
    login(username.value, data.access, data.refresh)

    // Clear error and redirect to orders list
    error.value = ''
    router.push('/orders')
  } catch (err) {
    error.value = 'Invalid credentials'
  }
}
</script>
