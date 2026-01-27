# Medical Backend System

A production-ready Flask backend application for managing medical clinic operations. This system provides a RESTful API for managing users, doctors, departments, availability, and appointment scheduling, built with a clean layered architecture and containerized with Podman.

## 🚀 Technology Stack

### Core Frameworks & Libraries
- **Language**: Python 3.10+
- **Web Framework**: Flask
- **Database ORM**: SQLAlchemy (Flask-SQLAlchemy)
- **Migrations**: Alembic (Flask-Migrate)
- **Serialization**: Marshmallow (Flask-Marshmallow)
- **Authentication**: JWT (PyJWT) - Stateless Token-based Auth
- **Containerization**: Podman & Podman Compose
- **Database**: PostgreSQL 15

### Testing & Documentation
- **Testing**: Pytest
- **API Documentation**: Swagger UI (flask-swagger-ui)

---

## ✨ Features

### Implementing Core Systems
- **Layered Architecture**: Separation of concerns (Controllers, Services, Repositories, Models).
- **Authentication**: User Registration, Login, JWT Token generation.
- **RBAC (Role-Based Access Control)**:
  - **Admin**: Full access (Manage departments, doctors).
  - **Doctor**: Manage availability, view appointments.
  - **Member**: Book appointments.
- **Department Management**: CRUD operations for clinic departments.
- **Doctor Onboarding**: Admin can register new doctors and assign them to departments.

### Implementing Appointment System
- **Doctor Availability**: Doctors can set their weekly working hours and slot duration.
- **Appointment Booking**: Members can book appointments with doctors.
- **Conflict Prevention**: 
  - System checks availability windows.
  - **Database constraints** prevent double-booking the same doctor at the same time.
- **My Appointments**: Users can view their own appointment history.

---

## 🛠️ Prerequisites

Ensure you have the following installed on your system:
- **Podman** (Docker Desktop alternative)
- **Podman Compose** (or Docker Compose)
- **Git**

---

## 🏃‍♂️ How to Run the Application

### 1. Clone the Repository
```bash
git clone <repository_url>
cd medical-backend-flask
```

### 2. Environment Configuration
The project uses environment variables for configuration. A basic setup is provided in `docker/podman-compose.yml`, but for local development, you can create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql+psycopg2://postgres:username@localhost:5432/db_name

# Security
SECRET_KEY=your-super-secret-key-change-me
```
*Note: When running with Podman Compose, the database credentials are automatically handled.*

### 3. Build and Start Containers
Use `podman-compose` to build the images and start the services (API + PostgreSQL).

```bash
# Start in detached mode
podman-compose -f docker/podman-compose.yml up -d --build
```

### 4. Database Migrations
The database schema is managed via Flask-Migrate. **Do not run `db.create_all()` manually.**

Run the migrations inside the container to set up the schema:
```bash
# Apply migrations to the database
podman exec medical-api flask db upgrade
```

### 5. Access the Application
- **API Root**: `http://localhost:5000/`
- **Swagger Documentation**: `http://localhost:5000/docs`

---

## 📖 API Documentation

The interactive Swagger UI is available at `http://localhost:5000/docs`. Provides detailed information on all endpoints, request payloads, and response schemas.

### Key Endpoints

#### Authentication
- `POST /auth/register`: Register a new user (Member/Admin/Doctor).
- `POST /auth/login`: Login and receive JWT access token.

#### Availability (Doctor Only)
- `POST /api/availability`: Set working hours for a specific day.
- `GET /api/availability/{doctor_id}`: View a doctor's availability.

#### Appointments
- `POST /api/appointments`: Book a slot (Member only).
- `GET /api/appointments`: View your appointments.

#### Admin
- `POST /admin/departments`: Create a department.
- `POST /admin/doctors`: Onboard a new doctor.
- `POST /admin/assign-doctor`: Assign a doctor to a department.

---

## 📂 Project Structure

```
medical-backend-flask/
├── app/
│   ├── controllers/     # Route handlers (Input parsing, Response formatting)
│   ├── services/        # Business logic (Validation, Complex rules)
│   ├── repositories/    # Database access (Queries, CRUD)
│   ├── models/          # SQLAlchemy Database Models
│   ├── schemas/         # Marshmallow Validation Schemas
│   └── security/        # JWT & Decorators
├── docker/              # Container configuration (podman-compose.yml)
├── migrations/          # Alembic migration scripts
├── tests/               # Pytest Unit/Integration tests
├── requirements.txt     # Python Dependencies
├── run.py               # Application Entrypoint
└── README.md            # Project Documentation
```

## 🐛 Troubleshooting

**Issue**: Migration says "No changes detected" but tables are missing?  
**Fix**: Ensure `app/__init__.py` calls `migrate.init_app(app, db)` and that your models are imported in `app/models/__init__.py`.

**Issue**: `podman-compose` fails to find the file?  
**Fix**: Run command from root: `podman-compose -f docker/podman-compose.yml up`.
