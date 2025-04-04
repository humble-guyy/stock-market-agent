import os
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import router as api_router
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Lifespan event handler using FastAPI's recommended approach
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Stock Market AI Agent API...")
    yield
    logger.info("Shutting down Stock Market AI Agent API...")

# Create FastAPI instance with lifespan support
app = FastAPI(title="Stock Market AI Agent API", lifespan=lifespan)
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
