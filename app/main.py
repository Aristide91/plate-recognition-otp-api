from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title="FastAPI Backend for Plate Recognition and OTP Verification",
    version="1.0.0",
    description="Backend services for vehicle license plate recognition (OCR), Keycloak authentication, and OTP verification (email/SMS).",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/", tags=["Health Check"])
async def read_root():
    return {"message": "Welcome to the FastAPI Backend!"}

from app.api.v1.endpoints import auth, vehicles, otp, admin

# Include API routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(vehicles.router, prefix="/api/v1/vehicles", tags=["License Plates"])
app.include_router(otp.router, prefix="/api/v1/otp", tags=["OTP"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
