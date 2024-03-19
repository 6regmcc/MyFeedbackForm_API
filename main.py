from fastapi import FastAPI
from fastapi.responses import JSONResponse

from core.database import Base, engine
from users.routes import router as guest_router, user_router
from auth.routes import router as auth_router
from surveys.routes import router as surveys_router
from surveys.pages.pages_routes import router as pages_router
from surveys.pages.questions.questions_routes import router as questions_router
from starlette.middleware.authentication import AuthenticationMiddleware
from core.security import JWTAuth
from starlette.middleware.cors import CORSMiddleware
import uvicorn



Base.metadata.create_all(engine)


app = FastAPI()
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(surveys_router)
app.include_router(pages_router)
app.include_router(questions_router)

app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())

origins = ["http://localhost:6006", "http://localhost:5173", "http://localhost:5174"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


@app.get('/')
def root():
    return {"status": "Running"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)