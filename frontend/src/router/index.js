import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '../views/HomeView.vue'
import OrdersList from '../views/OrdersList.vue'
import OrderDetail from '../views/OrderDetail.vue'
import LoginView from '../views/LoginView.vue'
import OrderEdit from '../views/OrderEdit.vue'
import OrderCreate from '../views/OrderCreate.vue'
import ProductsList from '../views/ProductsList.vue'
import ProductDetail from '../views/ProductDetail.vue'
import ProductEdit from '../views/ProductEdit.vue'
import ProductCreate from '../views/ProductCreate.vue'


const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/orders', name: 'orders', component: OrdersList },
  { path: '/orders/:id', name: 'order-detail', component: OrderDetail },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/orders/:id/edit', name: 'order-edit', component: OrderEdit },
  { path: '/orders/new', name: 'order-create', component: OrderCreate },
  { path: '/products', name: 'products', component: ProductsList },
  { path: '/products/:id', name: 'product-detail', component: ProductDetail },
  { path: '/products/:id/edit', name: 'product-edit', component: ProductEdit },
  { path: '/products/create', name: 'product-create', component: ProductCreate }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  // If the user is logged in and goes to /login → redirect to /orders
  if (to.path === '/login' && token) {
    return next('/orders')
  }

  // Allow only public pages if not logged in
  const publicPages = ['/', '/login']
  const authRequired = !publicPages.includes(to.path)

  if (authRequired && !token) {
    return next('/login')
  }

  // Everything is ok
  next()
})

  
