from fastapi import FastAPI
from src.database.config import Base, engine
from src.routes import blockchain  # Import the blockchain routes
from contextlib import asynccontextmanager
from src.blockchain.blockchain import start_blockchain

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    start_blockchain
    yield
    
# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)

app.include_router(blockchain.router, prefix="/api", tags=["Blockchain"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Blockchain API"}
