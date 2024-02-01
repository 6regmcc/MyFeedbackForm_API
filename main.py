from fastapi import FastAPI
from fastapi.responses import JSONResponse
from users.routes import router as guest_router, user_router
from auth.routes import router as auth_router
from starlette.middleware.authentication import AuthenticationMiddleware
from core.security import JWTAuth



app = FastAPI()
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())

@app.get('/')
def root():
    return {"status": "Running"}
