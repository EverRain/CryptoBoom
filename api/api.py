from fastapi import FastAPI, Depends
from routes import auth
from dependencies import get_current_user
from schemas.user import UserResponse

app = FastAPI()
app.include_router(auth.router)

@app.get("/me", response_model=UserResponse)
def read_current_user(current_user = Depends(get_current_user)):
    return current_user
