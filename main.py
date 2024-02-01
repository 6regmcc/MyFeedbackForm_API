from fastapi import FastAPI
from fastapi.responses import JSONResponse
from users.routes import router as user_router
from auth.routes import router as auth_router


app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)


@app.get('/')
def root():
    return {"status": "Running"}
