from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
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
    
@router.get("/visualize_donation/", response_class=HTMLResponse)
async def submit_donation_form(request: Request):
    return templates.TemplateResponse(
        name="donation_form.html", 
        context={"request": request}
    )
    
@router.post("/submit_donation/")
def add_donation(
    name: str = Form(...),
    sender: str = Form(...),
    receiver: str = Form(...),
    amount: int = Form(...),
    description: str = Form(""),
    transaction_id: str = Form(...),
    db: Session = Depends(get_db)
):
    # Create a Donation object
    # Create a Donation object
    donation = DonationCreate(
        name=name,
        sender=sender,
        receiver=receiver,
        amount=amount,
        description=description,
        transaction_id=transaction_id,
    )

    # Add the donation to the blockchain
    blockchain = DonationBlockchain(db)
    blockchain.add_block([donation])

    return RedirectResponse(url="/api/visualize/", status_code=303)