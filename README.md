# 🏠 Nestify — Luxury Apartment Management Platform

A modern full-stack SaaS application for managing luxury apartment societies.

Built using React, FastAPI, PostgreSQL, and Docker to demonstrate real-world backend architecture, multi-tenancy, authentication systems, and production-style project structure.

---

# 🎯 Overview

Nestify is a multi-tenant apartment management system where each society gets its own isolated workspace.

It supports:

- Role-based dashboards
- Maintenance billing with auto late fee calculation
- Complaint tracking
- Visitor approval workflow
- Facility booking with conflict prevention
- Notice board
- Community polls & voting
- Premium glassmorphism UI
- Dark / Light mode

This project simulates how real-world society management SaaS platforms operate.

---

# 🧰 Tech Stack

## Frontend
- React 18
- TypeScript
- Vite
- TailwindCSS
- Framer Motion
- Recharts
- Radix UI

## Backend
- FastAPI
- Python 3.11
- SQLAlchemy ORM
- Alembic (Database migrations)
- Pydantic

## Database
- PostgreSQL 15

## Authentication
- JWT (access tokens)
- Google OAuth2
- Phone OTP (mock implementation)
- Role-based access control

## DevOps
- Docker
- Docker Compose

---

# 🏗 Architecture Overview

Frontend (React)
        ↓
FastAPI Backend
        ↓
PostgreSQL Database

- Multi-tenant architecture using `society_id`
- JWT-based stateless authentication
- Modular router-based backend structure
- Alembic for version-controlled database migrations
- Dockerized services for consistent environments

---

# 🚀 Quick Start

## 1️⃣ Clone Repository

```bash
git clone https://github.com/epavan162/NESTIFY.git
cd NESTIFY
```

---

## 2️⃣ Environment Configuration

The `.env` file is already configured for local development.

```env
POSTGRES_USER=nestify
POSTGRES_PASSWORD=nestify123
POSTGRES_DB=nestify
DATABASE_URL=postgresql://nestify:nestify123@db:5432/nestify
JWT_SECRET=change-this-in-production
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173
```

For production:
- Change JWT_SECRET
- Add real Google OAuth credentials
- Use secure database credentials

---

## 3️⃣ Start All Services

```bash
docker-compose up --build
```

---

## 4️⃣ Access the Application

Frontend  
http://localhost:5173  

Backend API (Swagger Docs)  
http://localhost:8000/api/docs  

PostgreSQL  
localhost:5432  

On first startup:
- Database migrations run automatically
- Demo data is seeded automatically

---

# 🔑 Demo Credentials

## Admin
Email: admin@nestify.com  
Password: admin123  

Full system access.

---

## Residents
Emails:
- priya@nestify.com
- amit@nestify.com
- sneha@nestify.com
- vikram@nestify.com
- ananya@nestify.com
- rohit@nestify.com

Password: resident123  

Access: Personal dashboard, complaints, bookings, payments, polls.

---

## Security
Email: security@nestify.com  
Password: security123  

Access: Visitor entry/exit and approvals.

---

## Treasurer
Email: treasurer@nestify.com  
Password: treasurer123  

Access: Maintenance billing, payments management.

---

# ✨ Core Features

## 🔐 Authentication & Authorization

- Email + password login (bcrypt hashing)
- Phone OTP login (mock)
- Google OAuth2 login
- JWT-based sessions
- Role-based access:
  - Admin
  - Resident
  - Security
  - Treasurer

---

## 📊 Dashboards

### Admin Dashboard
- Total collection overview
- Pending dues tracking
- Resident count
- Complaint distribution
- Monthly revenue analytics

### Resident Dashboard
- Personal outstanding bills
- Payment history
- Complaint status
- Recent invoices

---

# 🏢 Core Modules

## Society Management
- Create societies
- Add towers
- Add flats
- Hierarchical structure

## Resident Management
- Add residents
- Assign flats
- Owner/Tenant status
- Move-in / Move-out tracking

## Maintenance Billing
- Generate monthly invoices
- Automatic 10% late fee on overdue payments
- Record payments (UPI / Card / Cash / Bank)
- Track payment history

## Complaint Management
- Submit complaints
- Priority levels
- Assign staff
- Status flow:
  Open → In Progress → Resolved

## Visitor Management
- Log visitor entry
- Resident approval workflow
- Vehicle tracking
- Checkout system

## Notice Board
Post announcements under:
- General
- Event
- Maintenance
- Emergency

## Facility Booking
Book shared amenities:
- Gym
- Pool
- Party Hall
- Tennis Court
- Clubhouse

Prevents double booking automatically.

## Polls & Voting
- Create community polls
- Cast votes
- View live results
- One vote per user enforcement

---

# 🗃 Database Schema

Nestify uses 12 PostgreSQL tables:

- societies
- towers
- flats
- users
- maintenance_invoices
- payments
- complaints
- visitors
- notices
- bookings
- polls
- votes

## Key Relationships

- Society → Towers → Flats → Users
- Invoice → Payments
- Poll → Votes
- All business tables linked using `society_id` for multi-tenancy
- Payments linked to invoices (many-to-one)
- Votes linked to polls (many-to-one, unique per user)

---

# 📡 API Endpoints

Interactive documentation:
http://localhost:8000/api/docs

## Authentication
- POST /login
- POST /register
- POST /otp/send
- POST /otp/verify
- GET /google/url
- GET /me

## Societies
- GET /
- POST /
- GET /{id}
- GET /{id}/towers
- POST /towers
- POST /flats

## Residents
- GET /
- GET /{id}
- PUT /{id}
- POST /{id}/assign-flat
- POST /{id}/move-out

## Maintenance
- GET /invoices
- POST /invoices
- GET /payments
- POST /payments

## Complaints
- GET /
- POST /
- PUT /{id}

## Visitors
- GET /
- POST /
- PUT /{id}/approve
- PUT /{id}/checkout

## Notices
- GET /
- POST /
- DELETE /{id}

## Bookings
- GET /
- POST /
- DELETE /{id}

## Polls
- GET /
- POST /
- POST /{id}/vote

## Dashboard
- GET /admin
- GET /resident

---

# 🛠 Development Commands

Start services:
```bash
docker-compose up --build
```

Run in background:
```bash
docker-compose up -d
```

View backend logs:
```bash
docker logs nestify-backend -f
```

View frontend logs:
```bash
docker logs nestify-frontend -f
```

Access PostgreSQL:
```bash
docker exec -it nestify-db psql -U nestify -d nestify
```

Stop services:
```bash
docker-compose down
```

Reset database completely:
```bash
docker-compose down -v
docker-compose up --build
```

---

# 📦 Pre-loaded Demo Data

The seed script automatically creates:

- 2 Societies
- 4 Towers
- 40 Flats
- 10 Users (all roles)
- 48 Maintenance Invoices
- Payments
- Complaints (various statuses)
- Visitors (pending, approved, checked out)
- Notices
- Facility bookings
- Polls with votes

---

# 🎨 UI/UX Features

- Glassmorphism design
- Smooth animations
- Role-based sidebar navigation
- Loading skeletons
- Toast notifications
- Fully responsive (mobile + desktop)
- Dark / Light theme toggle with persistence

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

Built as a full-stack SaaS-style project to demonstrate:

- Backend architecture
- Database design
- Multi-tenancy
- Authentication systems
- Production-style folder structure
- Dockerized environments

---
