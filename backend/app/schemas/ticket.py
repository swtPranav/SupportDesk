from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TicketCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=100)
    customer_email: EmailStr
    subject: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=1)
    priority: str = Field(default="Medium")


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
    created_at: datetime
    updated_at: datetime

class TicketListResponse(BaseModel):
    tickets: list[TicketResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

class TicketAssignment(BaseModel):
    assigned_to: int | None = None