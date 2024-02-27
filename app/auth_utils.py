from fastapi import HTTPException, Depends, Header, Request
from .auth import verify_token
from typing import List
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from jose import JWTError
from functools import wraps

security_scheme = HTTPBearer()

# Verifica si el usuario tiene el rol permitido
def has_permission(roles: List[str], allowed_roles: List[str]) -> bool:
    for role in roles:
        if role in allowed_roles:
            return True        
    return False


# Decorador para proteger rutas por roles
oauth2_scheme = HTTPBearer(scheme_name="Bearer")

def auth_required(roles=None):
    async def wrapper(token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
        try:
            payload = verify_token(token)

            if payload is False:
                raise HTTPException(status_code=401, detail='Invalid authorization token')
            
            user_roles = payload.get("role")

            if not has_permission(user_roles, roles):
                raise HTTPException(status_code=403, detail='User does not have permission to access this resource')
            
        except JWTError:
            raise HTTPException(status_code=401, detail='Invalid authorization token')

    return wrapper