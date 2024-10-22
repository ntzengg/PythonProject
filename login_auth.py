from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import schemas, models, database
from otp import generate_otp
from email_utils import send_otp_email
from auth import create_access_token
from database import get_db

router = APIRouter(
    prefix="/login_auth",
    tags=["login_auth"],
)

@router.post("/send_otp")
async def send_otp(email: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    otp = generate_otp()
    otp_data = models.OTPData(email=email, otp=otp, timestamp=datetime.utcnow())
    db.add(otp_data)
    db.commit()
    background_tasks.add_task(send_otp_email, email, otp)
    return {"message": "OTP sent to your email"}

@router.post("/verify_otp")
async def verify_otp(otp_request: schemas.OTPRequest, db: Session = Depends(get_db)):
    otp_data = db.query(models.OTPData).filter(models.OTPData.email == otp_request.email).first()
    if not otp_data or otp_data.otp != otp_request.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )
    
    if datetime.utcnow() > otp_data.timestamp + timedelta(minutes=5):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP has expired"
        )
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": otp_request.email}, expires_delta=access_token_expires
    )
    
    db.delete(otp_data)
    db.commit()
    
    return {"access_token": access_token, "token_type": "bearer"}
