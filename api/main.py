from fastapi import FastAPI
from src.database.config import Base, engine
from src.routes import blockchain  # Import the blockchain routes

# Initialize FastAPI app
app = FastAPI()

# Include blockchain-related routes
app.include_router(blockchain.router, prefix="/api", tags=["Blockchain"])

# Initialize database tables
@app.on_event("startup")
def init_db():
    Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Welcome to the Blockchain API"}
