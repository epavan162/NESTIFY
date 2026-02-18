# 🏠 Nestify — Luxury Apartment Management Platform

A full-stack web application for managing luxury apartment societies. Built as a personal project to explore modern web technologies and full-stack development practices.

![License](https://img.shields.io/badge/license-MIT-blue)
![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)

---

## 🎯 Overview

Nestify is a complete apartment/society management solution designed for luxury residential complexes. It provides role-based dashboards, maintenance billing with auto late-fee calculation, visitor management, complaint tracking, facility booking with conflict prevention, a notice board, and a community voting system — all wrapped in a premium glassmorphism UI.

---

## 🧰 Tech Stack

| Layer | Technology |
|-------------|-----------|
| **Frontend** | React 18, TypeScript, Vite, TailwindCSS, Framer Motion, Recharts, Radix UI |
| **Backend** | FastAPI, Python 3.11, SQLAlchemy ORM, Alembic (migrations) |
| **Database** | PostgreSQL 15 |
| **Auth** | JWT, Google OAuth2, Phone OTP (mock) |
| **DevOps** | Docker, Docker Compose |

---

## 🚀 Quick Start

### Prerequisites

- [Docker](https://www.docker.com/get-started) & Docker Compose installed

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd NESTIFY
```

### 2. Configure Environment

The `.env` file is pre-configured for local development. For production, update the values:

```bash
# .env (pre-configured — no changes needed for local dev)
POSTGRES_USER=nestify
POSTGRES_PASSWORD=nestify123
POSTGRES_DB=nestify
DATABASE_URL=postgresql://nestify:nestify123@db:5432/nestify
JWT_SECRET=your-super-secret-jwt-key-change-in-production
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173
```

### 3. Start All Services

```bash
docker-compose up --build
```

### 4. Access the App

| Service | URL |
|---------|-----|
| 🌐 **Frontend** | http://localhost:5173 |
| 📡 **Backend API (Swagger)** | http://localhost:8000/api/docs |
| 🗄️ **PostgreSQL** | `localhost:5432` |

> On first startup, the database is auto-migrated and seeded with comprehensive demo data.

---

## 🔑 Demo Credentials

| Role | Email | Password | Access |
|------|-------|----------|--------|
| **Admin** | `admin@nestify.com` | `admin123` | Full access — all modules, analytics dashboard, user management |
| **Resident** | `priya@nestify.com` | `resident123` | Personal dashboard, complaints, bookings, polls, invoices |
| **Resident** | `amit@nestify.com` | `resident123` | Same as above (different flat) |
| **Resident** | `sneha@nestify.com` | `resident123` | Same as above |
| **Resident** | `vikram@nestify.com` | `resident123` | Same as above |
| **Resident** | `ananya@nestify.com` | `resident123` | Same as above |
| **Resident** | `rohit@nestify.com` | `resident123` | Same as above |
| **Security** | `security@nestify.com` | `security123` | Visitor entry/exit, approval workflow |
| **Treasurer** | `treasurer@nestify.com` | `treasurer123` | Invoices, payments, billing management |

---

## ✨ Features

### 🔐 Authentication & Authorization
- Email/password login with bcrypt hashing
- Phone number + OTP (mock — OTP shown in toast notification & backend logs)
- Google OAuth2 (requires Google Cloud credentials)
- JWT token-based sessions with auto-refresh
- Role-based access control: **Admin**, **Resident**, **Security**, **Treasurer**

### 📊 Dashboards
- **Admin Dashboard** — Total collections, pending dues, resident count, complaint breakdown (pie chart), monthly collection trends (bar chart)
- **Resident Dashboard** — Personal pending bills, payment history, complaint status, recent invoices

### 🏢 Core Modules

| Module | Description |
|--------|-------------|
| **Society Management** | Create and manage societies, towers, and flats with hierarchical navigation |
| **Resident Management** | Add residents, assign to flats, track owner/tenant status, move in/out |
| **Maintenance Billing** | Generate monthly invoices, auto 10% late-fee on overdue, record payments (UPI/Card/Cash/Bank) |
| **Complaint System** | Submit complaints with priority levels, assign to staff, track status (open → in-progress → resolved) |
| **Visitor Management** | Log visitor entry/exit, resident approval workflow, vehicle tracking |
| **Notice Board** | Post announcements with categories (general, event, maintenance, emergency) |
| **Facility Booking** | Book amenities (Gym, Pool, Party Hall, Tennis Court, Clubhouse), automatic double-booking prevention |
| **Polls & Voting** | Create community polls, cast votes, live result visualization with animated bars |

### 🎨 UI/UX
- Dark/Light mode toggle with persistence
- Glassmorphism cards and design elements
- Animated sidebar with role-based navigation
- Smooth page transitions (Framer Motion)
- Loading skeletons for async content
- Toast notifications (Sonner)
- Fully responsive (mobile + desktop)

---

## 📁 Project Structure

```
NESTIFY/
├── .env                          # Environment variables
├── .gitignore                    # Git ignore rules
├── docker-compose.yml            # Docker orchestration
├── README.md
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt          # Python dependencies
│   ├── alembic.ini               # Migration config
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   │       └── 001_initial.py    # Initial DB migration (12 tables)
│   └── app/
│       ├── __init__.py
│       ├── main.py               # FastAPI entry point, CORS, router mounts
│       ├── config.py             # Pydantic settings (env vars)
│       ├── database.py           # SQLAlchemy engine, session, Base
│       ├── seed.py               # Comprehensive demo data seeder
│       ├── auth/
│       │   ├── deps.py           # get_current_user, require_role
│       │   ├── jwt.py            # Token create/verify
│       │   ├── oauth.py          # Google OAuth2 flow
│       │   └── otp.py            # Mock OTP service
│       ├── models/               # 12 SQLAlchemy ORM models
│       │   ├── society.py        # Society (top-level tenant)
│       │   ├── tower.py          # Tower → Society
│       │   ├── flat.py           # Flat → Tower
│       │   ├── user.py           # User (roles, auth, flat assignment)
│       │   ├── maintenance.py    # MaintenanceInvoice
│       │   ├── payment.py        # Payment → Invoice
│       │   ├── complaint.py      # Complaint (status, priority, assignment)
│       │   ├── visitor.py        # Visitor (entry/exit, approval)
│       │   ├── notice.py         # Notice (announcements)
│       │   ├── booking.py        # Booking (facility reservations)
│       │   └── poll.py           # Poll + Vote
│       ├── schemas/
│       │   └── schemas.py        # All Pydantic request/response schemas
│       └── routers/              # 10 API routers
│           ├── auth.py           # Register, login, OTP, OAuth
│           ├── societies.py      # Society/Tower/Flat CRUD
│           ├── residents.py      # Resident management
│           ├── maintenance.py    # Invoices & payments
│           ├── complaints.py     # Complaint CRUD
│           ├── visitors.py       # Visitor workflow
│           ├── notices.py        # Notice board
│           ├── bookings.py       # Facility booking
│           ├── polls.py          # Polls & voting
│           └── dashboard.py      # Admin & resident analytics
│
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── vite.config.ts            # Vite config with backend proxy
    ├── tsconfig.json
    ├── tailwind.config.ts        # Luxury design system
    ├── postcss.config.js
    ├── index.html
    └── src/
        ├── main.tsx              # React entry with router
        ├── App.tsx               # Routes, protected routes, providers
        ├── index.css             # Global styles, glassmorphism, animations
        ├── api/
        │   └── client.ts         # Axios client with JWT interceptor
        ├── store/
        │   ├── AuthContext.tsx    # Auth state management
        │   └── ThemeContext.tsx   # Dark/light mode
        ├── layouts/
        │   └── DashboardLayout.tsx  # Sidebar, header, role nav
        └── pages/
            ├── auth/LoginPage.tsx
            ├── dashboard/
            │   ├── AdminDashboard.tsx
            │   └── ResidentDashboard.tsx
            ├── society/SocietyPage.tsx
            ├── residents/ResidentsPage.tsx
            ├── maintenance/MaintenancePage.tsx
            ├── complaints/ComplaintsPage.tsx
            ├── visitors/VisitorsPage.tsx
            ├── notices/NoticesPage.tsx
            ├── bookings/BookingsPage.tsx
            └── polls/PollsPage.tsx
```

---

## 🗃️ Database Schema

PostgreSQL with **12 tables** managed via Alembic migrations:

```
societies ──┐
             ├── towers ──── flats ──── users
             ├── maintenance_invoices ──── payments
             ├── complaints
             ├── visitors
             ├── notices
             ├── bookings
             └── polls ──── votes
```

**Key relationships:**
- Multi-tenancy via `society_id` across all tables
- Users → Flats (one-to-many via `flat_id`)
- Payments → Invoices (many-to-one)
- Votes → Polls (many-to-one, unique per user)

---

## 📡 API Endpoints

Full interactive API docs available at http://localhost:8000/api/docs

| Group | Endpoints | Auth Required |
|-------|-----------|:---:|
| **Auth** | `POST /login`, `POST /register`, `POST /otp/send`, `POST /otp/verify`, `GET /google/url`, `GET /me` | Partial |
| **Societies** | `GET /`, `POST /`, `GET /{id}`, `GET /{id}/towers`, `POST /towers`, `POST /flats` | ✅ |
| **Residents** | `GET /`, `GET /{id}`, `PUT /{id}`, `POST /{id}/assign-flat`, `POST /{id}/move-out` | ✅ (Admin) |
| **Maintenance** | `GET /invoices`, `POST /invoices`, `GET /payments`, `POST /payments` | ✅ |
| **Complaints** | `GET /`, `POST /`, `PUT /{id}` | ✅ |
| **Visitors** | `GET /`, `POST /`, `PUT /{id}/approve`, `PUT /{id}/checkout` | ✅ |
| **Notices** | `GET /`, `POST /`, `DELETE /{id}` | ✅ |
| **Bookings** | `GET /`, `POST /`, `DELETE /{id}` | ✅ |
| **Polls** | `GET /`, `POST /`, `POST /{id}/vote` | ✅ |
| **Dashboard** | `GET /admin`, `GET /resident` | ✅ |

---

## 🔐 Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create an **OAuth 2.0 Client ID** (Web application)
3. Add authorized redirect URI: `http://localhost:8000/api/auth/google/callback`
4. Update `.env` with your `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`
5. Restart Docker: `docker-compose up --build`

---

## 🛠️ Development

```bash
# Start all services (with rebuild)
docker-compose up --build

# Start in detached mode
docker-compose up --build -d

# View backend logs
docker logs nestify-backend -f

# View frontend logs
docker logs nestify-frontend -f

# Access PostgreSQL directly
docker exec -it nestify-db psql -U nestify -d nestify

# Stop all services
docker-compose down

# Stop and remove all data (fresh start)
docker-compose down -v
```

### Reseed the Database

```bash
# Remove volumes to clear data, then rebuild
docker-compose down -v
docker-compose up --build
```

The seed script runs automatically on every fresh start (when no data exists).

---

## 📦 Pre-loaded Demo Data

The seed script creates comprehensive showcase data:

| Data | Count |
|------|-------|
| Societies | 2 |
| Towers | 4 |
| Flats | 40 |
| Users (all roles) | 10 |
| Maintenance Invoices | 48 (6 months × 8 flats) |
| Payments | ~40 |
| Complaints | 8 (various statuses & priorities) |
| Visitors | 8 (pending, approved, checked out) |
| Notices | 5 (events, maintenance, emergency) |
| Facility Bookings | 6 (Gym, Pool, Party Hall, etc.) |
| Polls | 3 (with 13 votes) |

---

## 📄 License

This project is licensed under the MIT License.
