from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.api import router as api_router
from app.core.config import DEBUG, PROJECT_NAME, VERSION

API_ROOT = "/api"


def get_application() -> FastAPI:
    app = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

    # CORS setting
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    return app


app = get_application()
