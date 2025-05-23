from fastapi import FastAPI
import uvicorn
import os
from pathlib import Path
from dotenv import load_dotenv

from src.core import uvicorn_options, app_settings
from src.api import api_router


env_path = Path('.') / ('.env.docker' if os.getenv('DOCKER_MODE') else '.env')
load_dotenv(env_path)

app = FastAPI(docs_url="/api/openapi")

app.include_router(api_router)

if __name__ == '__main__':
    print(uvicorn_options)
    uvicorn.run(
        "main:app",
        host=app_settings.host,
        port=app_settings.port,
        reload=app_settings.reload
    )
