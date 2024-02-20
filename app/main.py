from fastapi import FastAPI, Request, Response

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "La aplicacion esta funcionando!"}