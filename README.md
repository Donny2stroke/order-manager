
# Full Stack Order Manager

Technical test for the development of a full stack application consisting of a Django REST API backend and a Vue.js frontend for managing orders and related products.

The system allows full CRUD management of orders and products, with quantity support, search, filters, JWT authentication, soft delete, tests and automatic initialization via Docker.

---

## Table of contents
- [Implementation details](#implementation-details)
- [Project setup](#project-setup)
- [Frontend features](#frontend-features)
- [Backend features](#backend-features)
- [Testing](#testing)
- [Credentials](#credentials)
- [Test the application live](#hosted-deployment)

---

## Implementation details

The project simulates the backend and frontend of a basic order management system.  
It allows:
- Listing and searching orders by name, description or date
- Associating orders with products and quantities
- Managing the product catalog (creation, update, soft deletion)
- Authenticated access via JWT
- Responsive and user-friendly interface
- Automated Docker setup and seeding

### Technologies used
- **Backend**: Django 4.2 + Django REST Framework
- **Frontend**: Vue 3 + Vite + Bootstrap 5 + Font Awesome
- **Authentication**: JWT (SimpleJWT)
- **Containerization**: Docker & Docker Compose
- **Database**: SQLite (Django default)

---

## Project setup

### Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- (Optional for frontend only) Node.js v18+

---

### Run the full project via Docker

#### 1. Clone the repository

```bash
git clone https://github.com/Donny2stroke/order-manager.git
cd order-manager
```

#### 2. Run the full stack environment

```bash
docker compose up --build
```

> At first build, the system:
> - initializes the database
> - creates two users:
>   - `admin` (superuser)
>   - `frontend` (standard user)
> - prompts you to seed demo data if `RUN_SEED=y` is passed

Example:
```bash
RUN_SEED=y docker compose up --build
```

---

### Run backend locally (without Docker)

```bash
cd backend
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## Backend features

### Database model

- `Order`: name, description, date
- `Product`: name, price, is_active
- `OrderProduct`: intermediate model with quantity field (ManyToMany)

### Functionalities

- JWT Authentication (login, refresh, protected endpoints)
- Order creation with multiple products and quantities
- Order filtering (by date) and search (by name or description)
- Soft delete for products (they remain visible in order detail)
- Admin interface with tabular inline editing
- Swagger UI documentation (`/api/docs`)
- All endpoints available under `/api/`

### Why soft delete for products?

In this project, product deletion is handled via soft delete, meaning that when a product is "deleted", it is only marked as inactive (e.g. is_active = False) and excluded from active listings — but it is not physically removed from the database.

This design choice ensures data consistency for the Order entity.

Since each order contains references to the products that were available at the time of the transaction, deleting a product entirely would break the integrity of existing order data (e.g., orphaned product_id references in OrderProduct).
By using soft delete:
 - Existing orders continue to display the correct products
 - No risk of broken foreign key references or missing product info in order detail views



### Available API endpoints

| Method | Endpoint             | Description                    |
|--------|----------------------|--------------------------------|
| GET    | `/api/orders`        | List and filter orders         |
| POST   | `/api/orders`        | Create new order               |
| GET    | `/api/orders/<id>`   | View order details             |
| PUT    | `/api/orders/<id>`   | Edit order (products included) |
| DELETE | `/api/orders/<id>`   | Delete order                   |
| GET    | `/api/products`      | List all products              |
| POST   | `/api/products`      | Create a new product           |
| PUT    | `/api/products/<id>` | Edit product                   |
| DELETE | `/api/products/<id>` | Soft delete (disable product)  |

### Example payload (POST or PUT `/api/orders`)

```json
{
  "name": "Mario Rossi",
  "description": "Order for electronics",
  "date": "2025-05-17",
  "products_data": [
    { "product_id": 1, "quantity": 2 },
    { "product_id": 2, "quantity": 1 }
  ]
}
```

---

### Swagger documentation

- Schema JSON: [http://localhost:8000/api/schema](http://localhost:8000/api/schema)
- Swagger UI: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)

---

## Frontend features

### Stack

- Vue 3 (Composition API)
- Vite
- Bootstrap 5 (customizable via SCSS)
- Font Awesome
- Axios + Vue Router

### Main views

#### Orders
- View orders with search and date filter
- Create, update, delete orders with product selection and quantity
- Order detail page

#### Products
- View active and disabled products
- Create and update product info
- Soft delete and re-enable products

#### Auth & Navigation
- JWT login
- Authenticated routes only
- Logout and dynamic navbar
- Responsive navbar toggle

---

### Run frontend manually (without Docker)

```bash
cd frontend
npm install
npm run dev
```

Visit [http://localhost:5173](http://localhost:5173) in browser.  
Make sure the backend is running at `http://localhost:8000`.

---

### Environment configuration

Edit `.env` in `frontend/` to change backend base URL:

```
VITE_API_URL=http://localhost:8000/api
```

---

### Project structure

```
frontend/
├── views/             # Orders, Products, Login, Home
├── components/        # UI components
├── router/            # Vue Router with guards
├── stores/            # Auth logic (JWT tokens)
├── assets/            # SCSS, images, favicon
├── utils/             # Axios client
└── App.vue            # Main layout
```

---

## Testing

Run all backend tests with:

```bash
docker compose exec backend python manage.py test orders
```

Alternatively, you can run tests manually by entering the backend container:

```bash
docker compose up -d # Start services in background (if not already running)
docker compose exec backend bash
```

Once inside the container, execute:

```bash
python manage.py test orders
```


Tests cover:

- Authenticated access with JWT tokens
- Order creation with valid and invalid products
- Quantity and product validation
- Order update with new product list
- Detail view including related products


| Symbol  | Meaning                                |
| ------- | -------------------------------------- |
| `.`     | Test passed                            |
| `F`     | Test failed (`AssertionError`, etc.)   |
| `E`     | Error (`Exception`, unexpected crash)  |
| `s`     | Test skipped (`@skip`)                 |


---

## Credentials

| Role       | Username | Password      |
|------------|----------|---------------|
| Superuser  | admin    | admin         |
| Frontend   | frontend | frontend      |

---

## Hosted deployment

You can test the application live using the links below (Railway):

- **Frontend**: [https://robust-tranquility-production.up.railway.app](https://robust-tranquility-production.up.railway.app)
- **Backend**: [https://order-manager-production-dab7.up.railway.app](https://order-manager-production-dab7.up.railway.app)

Note:
The hosting environment is serverless. This means that both frontend and backend services automatically scale down and "sleep" after ~10 minutes of inactivity.
On first access, there may be a short delay of a few seconds while the server spins up.
Once activated, performance returns to normal for subsequent requests.

---