from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.ticket import Ticket
from app.models.user import User


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)


@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total_tickets = db.query(Ticket).count()

    open_tickets = (
        db.query(Ticket)
        .filter(Ticket.status == "Open")
        .count()
    )

    in_progress_tickets = (
        db.query(Ticket)
        .filter(Ticket.status == "In Progress")
        .count()
    )

    resolved_tickets = (
        db.query(Ticket)
        .filter(Ticket.status == "Resolved")
        .count()
    )

    closed_tickets = (
        db.query(Ticket)
        .filter(Ticket.status == "Closed")
        .count()
    )

    high_priority_tickets = (
        db.query(Ticket)
        .filter(Ticket.priority == "High")
        .count()
    )

    assigned_tickets = (
        db.query(Ticket)
        .filter(Ticket.assigned_to.isnot(None))
        .count()
    )

    unassigned_tickets = (
        db.query(Ticket)
        .filter(Ticket.assigned_to.is_(None))
        .count()
    )

    active_agents = (
        db.query(User)
        .filter(
            User.is_active == True,
            User.role == "agent",
        )
        .count()
    )

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "in_progress_tickets": in_progress_tickets,
        "resolved_tickets": resolved_tickets,
        "closed_tickets": closed_tickets,
        "high_priority_tickets": high_priority_tickets,
        "assigned_tickets": assigned_tickets,
        "unassigned_tickets": unassigned_tickets,
        "active_agents": active_agents,
    }