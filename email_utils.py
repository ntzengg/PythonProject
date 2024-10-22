import smtplib
import ssl
from fastapi import HTTPException
from email.message import EmailMessage
from email.utils import parseaddr
from otp import generate_otp


# Email configuration
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587  # Port for STARTTLS
EMAIL_ADDRESS = "netsmartzengg2001@hotmail.com"
EMAIL_PASSWORD = "Netsmartz@1386"

def send_email(email_address: str, subject: str, body: str):
    # Create the email message
    message = EmailMessage()
    message.set_content(body)
    message["Subject"] = subject
    message["From"] = EMAIL_ADDRESS
    message["To"] = email_address

    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)  # Secure the connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Login to the email server
            server.send_message(message)  # Send the email
        print("Email sent successfully")
    except Exception as e:
        print(f"An error occurred while sending the email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email")



async def send_otp_email(email: str, otp: str):
    # otp = generate_otp()
    subject = "Your OTP Code"
    body = f"Your OTP code is {otp}"
    send_email(email, subject, body)
    return otp  # Return OTP for storing it in the database
