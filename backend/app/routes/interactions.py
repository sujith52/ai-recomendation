from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import InteractionCreate, InteractionResponse, InteractionType
from app.models import Interaction, User, Item
from app.database import get_db



router = APIRouter(prefix="/interactions", tags=["interactions"])

@router.post("/", response_model=InteractionResponse)
def log_interaction(interaction: InteractionCreate, db: Session = Depends(get_db)):
    # Check if user and item exist
    user = db.query(User).filter(User.id == interaction.user_id).first()
    item = db.query(Item).filter(Item.id == interaction.item_id).first()

    if not user or not item:
        raise HTTPException(status_code=404, detail="User or Item not found")

    db_interaction = Interaction(
        user_id=interaction.user_id,
        item_id=interaction.item_id,
        interaction_type=interaction.interaction_type,
        timestamp=datetime.utcnow()
    )
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

@router.get("/", response_model=List[InteractionResponse])
def get_interactions(
    user_id: Optional[int] = None,
    item_id: Optional[int] = None,
    interaction_type: Optional[InteractionType] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Interaction)

    if user_id:
        query = query.filter(Interaction.user_id == user_id)
    if item_id:
        query = query.filter(Interaction.item_id == item_id)
    if interaction_type:
        query = query.filter(Interaction.interaction_type == interaction_type)

    return query.all()

