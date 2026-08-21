from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.permissions import require_admin
from app.database import get_db
from app.models.ticket import Ticket
from app.models.user import User
from app.dependencies import get_current_user
from app.models.note import Note
from app.schemas.ticket import (
    TicketAssignment,
    TicketCreate,
    TicketListResponse,
    TicketResponse,
    TicketUpdate,
)


router = APIRouter(
    prefix="/api/tickets",
    tags=["Tickets"],
)


def generate_ticket_id(db: Session) -> str:
    last_ticket = (
        db.query(Ticket)
        .order_by(Ticket.id.desc())
        .first()
    )

    if last_ticket is None:
        return "TKT-001"

    next_number = last_ticket.id + 1
    return f"TKT-{next_number:03d}"


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ticket_id = generate_ticket_id(db)

    new_ticket = Ticket(
        ticket_id=ticket_id,
        customer_name=ticket.customer_name,
        customer_email=ticket.customer_email,
        subject=ticket.subject,
        description=ticket.description,
        priority=ticket.priority,
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket

@router.get(
    "",
    response_model=TicketListResponse,
)
def get_tickets(
    search: str | None = Query(
        default=None,
        description="Search by customer name, email, subject, or description",
    ),
    status_filter: str | None = Query(
        default=None,
        alias="status",
        description="Filter by ticket status",
    ),
    priority: str | None = Query(
        default=None,
        description="Filter by ticket priority",
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Page number",
    ),
    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of tickets per page",
    ),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Ticket)

    # Search
    if search:
        search_term = f"%{search}%"

        query = query.filter(
            or_(
                Ticket.customer_name.ilike(search_term),
                Ticket.customer_email.ilike(search_term),
                Ticket.subject.ilike(search_term),
                Ticket.description.ilike(search_term),
            )
        )

    # Status filter
    if status_filter:
        query = query.filter(
            Ticket.status == status_filter
        )

    # Priority filter
    if priority:
        query = query.filter(
            Ticket.priority == priority
        )

    # Total matching tickets
    total = query.count()

    # Pagination
    offset = (page - 1) * page_size

    tickets = (
        query
        .order_by(Ticket.id.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    total_pages = ceil(total / page_size) if total else 0

    return {
        "tickets": tickets,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }

@router.get(
    "/{ticket_id}",
    response_model=TicketResponse,
)
def get_ticket(
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

    return ticket

@router.put(
    "/{ticket_id}",
    response_model=TicketResponse,
)
def update_ticket(
    ticket_id: str,
    ticket_data: TicketUpdate,
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

    if ticket_data.status is not None:
        ticket.status = ticket_data.status

    if ticket_data.priority is not None:
        ticket.priority = ticket_data.priority

    if ticket_data.subject is not None:
        ticket.subject = ticket_data.subject

    if ticket_data.description is not None:
        ticket.description = ticket_data.description

    db.commit()
    db.refresh(ticket)

    return ticket

@router.put(
    "/{ticket_id}/assign",
    response_model=TicketResponse,
)
def assign_ticket(
    ticket_id: str,
    assignment: TicketAssignment,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
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

    if assignment.assigned_to is not None:
        user = (
            db.query(User)
            .filter(
                User.id == assignment.assigned_to,
                User.is_active == True,
            )
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="Active user not found",
            )

    ticket.assigned_to = assignment.assigned_to

    db.commit()
    db.refresh(ticket)

    return ticket