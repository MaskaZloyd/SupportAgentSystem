from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from .tasks import publish_ticket_event
from . import config

app = FastAPI()

class Ticket(BaseModel):
    id: str
    description: str

@app.on_event("startup")
async def startup_event():
    print(f"Orchestrator Service started. Kafka configured at: {config.KAFKA_BOOTSTRAP_SERVERS}")


@app.post("/tickets")
async def create_ticket_endpoint(ticket: Ticket, background_tasks: BackgroundTasks):
    """
    Принимает новый тикет и ставит задачу на публикацию события.
    """
    print(f"Received ticket: {ticket.id}")
    background_tasks.add_task(publish_ticket_event, 'ticket.created', ticket.model_dump())
    return {"message": "Ticket received, processing started.", "ticket_id": ticket.id}

@app.get("/")
async def root():
    return {"message": "Orchestrator Service is running."}