from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.note import NoteResponse


class TicketCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=100)
    customer_email: EmailStr
    subject: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=1)
    priority: str = Field(default="Medium")


class PublicTicketResponse(BaseModel):
    ticket_id: str
    status: str


class TicketUpdate(BaseModel):
    status: str | None = None
    priority: str | None = None
    subject: str | None = None
    description: str | None = None


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ticket_id: str
    customer_name: str
    customer_email: EmailStr
    subject: str
    description: str
    status: str
    priority: str
    assigned_to: int | None = None
    created_at: datetime
    updated_at: datetime


class TicketDetailResponse(TicketResponse):
    notes: list[NoteResponse] = []

class TicketListResponse(BaseModel):
    tickets: list[TicketResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

class TicketAssignment(BaseModel):
    assigned_to: int | None = None
