from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.routers import auth, societies, residents, maintenance, complaints, visitors, notices, bookings, polls, dashboard

settings = get_settings()

app = FastAPI(
    title="Nestify API",
    description="Luxury Apartment Management Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(societies.router, prefix="/api/societies", tags=["Societies"])
app.include_router(residents.router, prefix="/api/residents", tags=["Residents"])
app.include_router(maintenance.router, prefix="/api/maintenance", tags=["Maintenance"])
app.include_router(complaints.router, prefix="/api/complaints", tags=["Complaints"])
app.include_router(visitors.router, prefix="/api/visitors", tags=["Visitors"])
app.include_router(notices.router, prefix="/api/notices", tags=["Notices"])
app.include_router(bookings.router, prefix="/api/bookings", tags=["Bookings"])
app.include_router(polls.router, prefix="/api/polls", tags=["Polls"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])


@app.get("/api/health")
def health_check():
    return {"status": "healthy", "app": "Nestify API", "version": "1.0.0"}
