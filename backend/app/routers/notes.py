from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.note import Note
from app.models.ticket import Ticket
from app.schemas.note import NoteCreate, NoteResponse


router = APIRouter(
    prefix="/api/tickets/{ticket_id}/notes",
    tags=["Notes"],
)


@router.post(
    "",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_note(
    ticket_id: str,
    note_data: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = (
        db.query(Ticket)
        .filter(Ticket.ticket_id == ticket_id)
        .first()
    )

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    note = Note(
        ticket_id=ticket_id,
        note_text=note_data.content,
        content=note_data.content,
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    return note

@router.get(
    "",
    response_model=list[NoteResponse],
)
def get_ticket_notes(
    ticket_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket = (
        db.query(Ticket)
        .filter(Ticket.ticket_id == ticket_id)
        .first()
    )

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    notes = (
        db.query(Note)
        .filter(Note.ticket_id == ticket_id)
        .order_by(Note.created_at.desc())
        .all()
    )

    return notes

@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_note(
    ticket_id: str,
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = (
        db.query(Note)
        .filter(
            Note.id == note_id,
            Note.ticket_id == ticket_id,
        )
        .first()
    )

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found",
        )

    db.delete(note)
    db.commit()

    return None