from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserOut
from app.db.session import get_db
from app.services.user_service import create_user, authenticate_user, get_user_by_email
from app.utils.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from sqlalchemy import inspect
from app.db.models import User  



router = APIRouter()

def ensure_users_table_exists(db: Session):
    inspector = inspect(db.bind)
    if 'users' not in inspector.get_table_names():
        print("Users table does not exist, creating it now.")
        User.__table__.create(db.bind)

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
