from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models.user import User
from models import get_db
from utils.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        pseudo = payload.get("sub")
        if pseudo is None:
            raise HTTPException(status_code=401, detail="Token invalide")
        user = db.query(User).filter(User.pseudo == pseudo).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        return user
    except JWTError:
        raise HTTPException(status_code=403, detail="Impossible de valider les identifiants")
