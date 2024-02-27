from app.routes.user import router as user_router
from app.routes.auth import router as auth_router
from fastapi import FastAPI, Request, Response

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "La aplicacion esta funcionando!"}


app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])