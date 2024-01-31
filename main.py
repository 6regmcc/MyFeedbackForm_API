from fastapi import FastAPI
from fastapi.responses import JSONResponse
from users.routes import router as user_router


app = FastAPI()
app.include_router(user_router)


@app.get('/')
def root():
    return {"status": "Running"}
