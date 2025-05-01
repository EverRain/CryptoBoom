from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserLogin, UserResponse
from utils.security import hash_password, verify_password, create_access_token
from models import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.pseudo == user.pseudo).first():
        raise HTTPException(status_code=400, detail="Pseudo déjà utilisé")
    new_user = User(
        pseudo=user.pseudo,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.pseudo == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    access_token = create_access_token(data={"sub": user.pseudo})
    return {"access_token": access_token, "token_type": "bearer"}
