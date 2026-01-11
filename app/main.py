from fastapi import FastAPI
from app.routes.auth_routes import router as auth_router

app = FastAPI(title="FastAPI MongoDB Auth")

app.include_router(auth_router)

@app.get("/")
def root():
    return {"status": "Authentication API running"}
