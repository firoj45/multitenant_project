# Django Multi-Tenant API Project

This is a Django-based multi-tenant API application demonstrating a hierarchical structure:
- **Tenant**
- **Organization**
- **Department**
- **Customer**

Authentication is handled via Token-based authentication. Each request must include a custom header for tenant domain.

---

#Features

- Token-based user authentication
- Multi-tenant data isolation
- Hierarchical model relationships
- Full CRUD support via Django REST Framework
- API-first interface
- Unit tests for core functionalities

---

## Project Structure

```bash
multitenant_project/
│
├── core_app/
│   ├── models.py          # Tenant, Organization, Department, Customer models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # ViewSets with tenant isolation logic
│   ├── urls.py            # API routing
│   ├── tests/             # DRF test cases
│
├── multitenant_project/
│   ├── settings.py
│   ├── urls.py
│   ├── middleware.py      # TenantMiddleware for per-request isolation
│
└── manage.py

1. Create virtual environment
  python3 -m venv venv
  source venv/bin/activate
2. Install dependencies
  pip install -r requirements.txt
3. Configure the database (PostgreSQL)
  CREATE DATABASE multitenant_db;
  CREATE USER multitenant_user WITH PASSWORD 'your_pass';
  GRANT ALL PRIVILEGES ON DATABASE multitenant_db TO multitenant_user;
  #Update settings.py:
4. Run migrations
  python manage.py makemigrations
  python manage.py migrate
5. Run the server
  python manage.py runserver
6. API Usage
  Use the following headers in each request:
  Authorization: Token <your-token>
  X-Tenant-Domain: tenant1.com
  Example: Create Organization
  
  POST /api/organizations/
  Headers:
    Authorization: Token abc123
    X-Tenant-Domain: tenant1.com
  
  Body:
  {
  "tenant": 1,
  "name": "Acme Corp"
  }
7. Running Tests
  python manage.py test

8. Postman collection added for all of the API's
9. Admin Panel with filter
10. DRF View