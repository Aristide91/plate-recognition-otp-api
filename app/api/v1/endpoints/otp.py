from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.services.otp_service import otp_service
from app.database import create_connection, create_reservation
from datetime import datetime
from app.core.security import get_current_user

router = APIRouter()

class SendOTPRequest(BaseModel):
    phone_number: Optional[str] = Field(None, pattern=r"^\+\d{10,15}$")
    email: Optional[EmailStr] = None

class VerifyOTPRequest(BaseModel):
    identifier: str
    otp_code: str = Field(..., min_length=6, max_length=6)
    plate: str
    vin: str


@router.post("/send-otp", summary="Send OTP to phone number or email", response_model=dict)
async def send_otp(request: SendOTPRequest, current_user: dict = Depends(get_current_user)):
    """
    Generates and sends an OTP code to the provided phone number or email address.
    Requires authentication.
    """
    otp_code = otp_service.generate_otp()
    success = False
    identifier = None

    if request.phone_number:
        success = await otp_service.send_otp_sms(request.phone_number, otp_code)
        identifier = str(request.phone_number).strip().lower()
    elif request.email:
        success = await otp_service.send_otp_email(request.email, otp_code)
        identifier = str(request.email).strip().lower()
    else:
        raise HTTPException(status_code=400, detail="Must provide either a phone_number or an email.")

    if success:
        otp_service.store_otp(identifier, otp_code)
        print(f"--- DEBUG : OTP {otp_code} stocké pour l'identifiant '{identifier}' ---")
        return {"message": "OTP sent successfully.", "identifier": identifier}
    else:
        raise HTTPException(status_code=500, detail="Failed to send OTP.")


@router.post("/verify-otp", summary="Verify OTP code", response_model=dict)
async def verify_otp(request: VerifyOTPRequest, current_user: dict = Depends(get_current_user)):
    """
    Verifies the provided OTP code and saves the reservation to the database.
    Requires authentication.
    """
    clean_identifier = str(request.identifier).strip().lower()
    clean_code = str(request.otp_code).strip()

    print(f"--- DEBUG : Tentative de vérification pour '{clean_identifier}' avec le code '{clean_code}' ---")

    if otp_service.verify_otp(clean_identifier, clean_code):
        conn = create_connection()
        if conn:
            reservation = (
                request.plate,
                request.vin,
                clean_identifier,
                "Validé",
                datetime.now().isoformat()
            )
            create_reservation(conn, reservation)
            conn.close()
        return {"message": "OTP verified successfully.", "identifier": clean_identifier}
    else:
        raise HTTPException(status_code=400, detail="Invalid OTP code or identifier.")