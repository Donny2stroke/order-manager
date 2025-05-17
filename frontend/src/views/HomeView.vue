<template>
  <div class="container py-5">
    <div class="text-center mb-5">
      <h1 class="display-4 fw-bold text-primary">Order Manager</h1>
      <p class="lead">Manage orders and products efficiently from a single interface.</p>
      <p class="text-muted">Create, update, search and organize everything with ease.</p>
    </div>

    <div class="row g-4">
      <div class="col-md-6">
        <div class="card h-100 shadow-sm border-0">
          <div class="row">
            <div class="col-6">
              <img src="/src/assets/ordersBanner.png" class="card-img-top" alt="Orders image" />
            </div>
            <div class="col-6">
              <div class="card-body d-flex flex-column justify-content-between">
                <h4 class="card-title">
                  Orders Management
                </h4>
                <p class="card-text">
                  Access a complete overview of all your customer orders. Create new orders, modify existing ones and associate products.
                </p>
                <router-link to="/orders" class="btn btn-outline-primary mt-3">
                  Go to Orders
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card h-100 shadow-sm border-0">
          <div class="row">
            <div class="col-6">
              <img src="/src/assets/productsBanner.png" class="card-img-top" alt="Orders image" />
            </div>
            <div class="col-6">
              <div class="card-body d-flex flex-column justify-content-between">
                <h4 class="card-title">
                  Products Management
                </h4>
                <p class="card-text">
                  Keep your product catalog always up to date. Add new products, modify names or prices, and deactivate unused ones.
                </p>
                <router-link to="/products" class="btn btn-outline-primary s mt-3">
                  Go to Products
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
