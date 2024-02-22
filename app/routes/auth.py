from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import Auth
from fastapi.responses import JSONResponse
from app.auth import equals_password, create_access_token

from app.services.user import get_user_by_email

router = APIRouter()

@router.post("/login")
async def login(auth: Auth, db: Session = Depends(get_db)):
    try:
        user = get_user_by_email(auth.email, db=db)
        if user is None:
            return JSONResponse(content={"message": "User mot found"},
                                status_code = status.HTTP_404_NOT_FOUND)
        
        validation_password = equals_password(password= auth.password, hash_password=user.hashed_password)
        if validation_password is False:
            return JSONResponse(content={"message": "Credenciales invalidas"},
                                status_code=status.HTTP_401_UNAUTHORIZED)
        
        roles = [role.nombre for role in user.roles]

        token = create_access_token({"username": user.email, "role": roles, "id": user.id})
        return {"token": token}
    
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=401, detail=e)