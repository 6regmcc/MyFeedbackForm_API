from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

from core.database import Base, engine
from users.routes import router as guest_router, user_router
from auth.routes import router as auth_router
from surveys.routes import router as surveys_router
from surveys.pages.pages_routes import router as pages_router
from surveys.pages.questions.questions_routes import router as questions_router
from responses.responses_routes import router as responses_router
from responses.resposnes_data_routes import router as responses_data_router
from starlette.middleware.authentication import AuthenticationMiddleware
from core.security import JWTAuth
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import uuid



Base.metadata.create_all(engine)


app = FastAPI()
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(surveys_router)
app.include_router(pages_router)
app.include_router(questions_router)
app.include_router(responses_router)
app.include_router(responses_data_router)

app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())

origins = ["http://localhost:6006", "http://localhost:5173", "http://localhost:5174"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "OPTIONS", "PUT", "DELETE"],
    allow_headers=["Content-Type", "x-requested-with", "Authorization", "Set-Cookie"],
    expose_headers=['Set-Cookie', 'Authorization', 'Origin', 'X-Requested-With', 'Content-Type', 'Accept']
)


@app.get('/')
def root():
    return {"status": "Running"}


@app.get("/test_cookie")
def get_session_cookie(response: Response):
    response.set_cookie(key="fakesession", value="sdfsdfsdf")
    return {"message": "Come to the dark side, we have cookies"}




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)