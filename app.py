from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, auth, database, login_auth
from database import engine, SessionLocal

# Create all tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configuration (if needed)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the auth router
app.include_router(auth.router)
app.include_router(login_auth.router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application with JWT and OTP authentication!"}

# Initialize and include the database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9999)
