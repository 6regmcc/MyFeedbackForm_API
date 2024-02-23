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
#test

Base.metadata.create_all(engine)


app = FastAPI()
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(surveys_router)
app.include_router(pages_router)
app.include_router(questions_router)

app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())

@app.get('/')
def root():
    return {"status": "Running"}
