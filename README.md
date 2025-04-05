Online Grocery Store
This is a Django-based Online Grocery Store application, designed to enable users to shop for groceries online. The project includes features like user authentication, product management, shopping cart functionality, order processing, and secure payment integration using Paystack.

1. Features
1.1. User Authentication
  - Sign-up, login, logout, and password reset functionalities.
  - User roles: Admin and Customer.

1.2. Product Management
  - CRUD operations for products and categories.
  - Filtering by name, category, and price.

1.3. Shopping Cart
  - Add, update, and remove items from cart.

1.4. Order Management
  - Place and track orders.
  - Admin view and manage orders.

1.5. Payment Integration
  - Secure checkout using Paystack.

1.6. Admin Panel
  - Manage users, products, and orders via Django Admin.

1.7. RESTful API
  - API for products, users, orders, and cart operations.

2. Technologies Used
2.1. Django
2.2. Django REST Framework
2.3. PostgreSQL
2.4. Paystack API
2.5. Bootstrap (optional for UI)

3. Setup and Installation
3.1. Clone the repository:

bash
Copy
Edit
git clone https://github.com/your-username/OnlineGroceryStore.git
cd OnlineGroceryStore
3.2. Create and activate virtual environment:

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate for Windows

3.3. Install dependencies:
pip install -r requirements.txt

3.4. Set up PostgreSQL database.
3.5. Add Paystack key in settings.py:
Edit
PAYSTACK_SECRET_KEY = 'your-secret-key'

3.6. Run migrations:
python manage.py migrate

3.7. Create superuser:
python manage.py createsuperuser

3.8. Start development server:
python manage.py runserver

3.9. Access app at http://127.0.0.1:8000

4. API Endpoints
4.1. User
  - POST /api/auth/register/
  - POST /api/auth/login/
  - POST /api/auth/logout/
  - POST /api/auth/password-reset/

4.2. Product
  - GET /api/products/
  - GET /api/products/{id}/
  - POST /api/products/ (Admin)
  - PUT /api/products/{id}/ (Admin)
  - DELETE /api/products/{id}/ (Admin)

4.3. Order
  - GET /api/orders/ (Admin)
  - POST /api/orders/ (Customer)
