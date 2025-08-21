from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.api.context.config import settings
from src.api.controller.routes import api_router

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router,prefix=settings.API_V1_STR)
app.mount("/comparisons", StaticFiles(directory="comparisons"), name="comparisons")


@app.get("/")
def root():
    return {"message": settings.PROJECT_NAME, "status": "running"}
