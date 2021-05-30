from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()

# CORS setting
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_ROOT = "/api"


@app.get("/")
async def index() -> dict:
    return {"test": "test"}


def main():
    uvicorn.run("app.main:app", port=8031, reload=True)


if __name__ == "__main__":
    main()
