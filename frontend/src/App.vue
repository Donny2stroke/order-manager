<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary px-4 shadow">
      <router-link class="navbar-brand fw-bold text-white" to="/">
        <font-awesome-icon icon="user" class="me-2" />
        Order Manager
      </router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#mainNavbar"
        aria-controls="mainNavbar"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="mainNavbar">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/orders">
              <font-awesome-icon icon="box" class="me-1" />
              Orders
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/products">
              <font-awesome-icon icon="tags" class="me-1" />
              Products
            </router-link>
          </li>
        </ul>

        <div class="d-flex align-items-center gap-2">
          <template v-if="auth.isLoggedIn">
            <span class="text-white">
              <font-awesome-icon icon="user" class="me-1" />
              Hi {{ auth.username }}
            </span>
            <button class="btn btn-outline-light btn-sm" @click="doLogout">
              <font-awesome-icon icon="sign-out-alt" class="me-1" />
              Logout
            </button>
          </template>
          <template v-else>
            <router-link class="btn btn-outline-light btn-sm" to="/login">
              <font-awesome-icon icon="sign-in-alt" class="me-1" />
              Login
            </router-link>
          </template>
        </div>
      </div>
    </nav>
    <main class="container py-4">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { auth, logout } from './stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()

const doLogout = () => {
  logout()
  router.push('/login')
}
</script>
