from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from ..database.config import SessionLocal
from ..blockchain.blockchain import DonationBlockchain
from ..schemas.donation import DonationCreate
from ..schemas.block import StoredDonationBlockResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/donations/")
def add_donation(donation: DonationCreate, db: Session = Depends(get_db)):
    blockchain = DonationBlockchain(db)
    blockchain.add_block([donation])
    return {"message": "Donation added and block created"}

@router.get("/blocks/", response_model=list[StoredDonationBlockResponse])
def get_blocks(db: Session = Depends(get_db)):
    blockchain = DonationBlockchain(db)
    return blockchain.chain

@router.get("/is_valid/")   
def is_valid(db: Session = Depends(get_db)):
    blockchain = DonationBlockchain(db)
    return {"is_valid": blockchain.is_chain_valid()}

@router.get("/visualize/", response_class=HTMLResponse)
async def visualize(request: Request, db: Session = Depends(get_db)):
    blockchain = DonationBlockchain(db)
    return templates.TemplateResponse(request=request, name="visualizer.html", context={"chain": blockchain.chain})
    