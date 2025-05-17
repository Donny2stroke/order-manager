
# Full Stack Order Manager

Technical test for the development of a full stack application consisting of a Django REST API backend and a Vue.js frontend for managing customer orders and related products.

The system allows full CRUD management of orders and products, with quantity support (many-to-many), search, filters, JWT authentication, soft delete, tests and automatic initialization via Docker.

---

## Table of contents
- [Implementation details](#implementation-details)
- [Project setup](#project-setup)
- [Frontend features](#frontend-features)
- [Backend features](#backend-features)
- [Testing](#testing)
- [Credentials](#credentials)
- [Resources consulted](#resources-consulted)

---

## Implementation details

The project simulates the backend and frontend of a basic e-commerce order management system.  
It allows:
- Listing and searching orders by customer name, description or date
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
git clone https://github.com/your-username/order-manager.git
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
- Soft delete for products (they remain visible in order history)
- Admin interface with tabular inline editing
- Swagger UI documentation (`/api/docs`)
- All endpoints available under `/api/`

### Available API endpoints

| Method | Endpoint           | Description                    |
|--------|--------------------|--------------------------------|
| GET    | `/api/orders`      | List and filter orders         |
| POST   | `/api/orders`      | Create new order               |
| GET    | `/api/orders/<id>` | View order details             |
| PUT    | `/api/orders/<id>` | Edit order (products included) |
| DELETE | `/api/orders/<id>` | Delete order                   |
| GET    | `/api/products`    | List all products              |
| POST   | `/api/products`    | Create a new product           |
| PUT    | `/api/products/<id>` | Edit product                |
| DELETE | `/api/products/<id>` | Soft delete (disable)       |

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

Tests cover:

- Authentication via JWT
- Order creation with valid/invalid products
- Product validation and quantity logic
- Deletion and update cases

---

## Credentials

| Role       | Username | Password      |
|------------|----------|---------------|
| Superuser  | admin    | admin         |
| Frontend   | frontend | frontend      |

---

## Hosted deployment (Railway)

You can test the application live using the links below:

- **Frontend**: [https://robust-tranquility-production.up.railway.app](https://robust-tranquility-production.up.railway.app)
- **Backend**: [https://order-manager-production-dab7.up.railway.app](https://order-manager-production-dab7.up.railway.app)

---

## Resources consulted

- [Django Docs](https://docs.djangoproject.com/en/4.2/)
- [DRF Docs](https://www.django-rest-framework.org/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)
- [Bootstrap 5 Docs](https://getbootstrap.com/)
- [Vue 3 Docs](https://vuejs.org/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Font Awesome Docs](https://fontawesome.com/docs/web/use-with/vue/)
- [Vue Router](https://router.vuejs.org/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Testing DRF](https://medium.com/@akshatgadodia/testing-django-and-django-rest-framework-drf-ensuring-reliability-236f0fcbeee6)
