from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict

from ai_engine import analyze_mcq_results, chat_with_maa

app = FastAPI(title="Maa - Mental Wellness Companion")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Template configuration
templates = Jinja2Templates(directory="templates")


# Request/Response schemas
class MCQRequest(BaseModel):
    answers: List[str]

class MCQResponse(BaseModel):
    mood: str
    maa_initial_message: str

class ChatRequest(BaseModel):
    message: str
    context: str
    history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    reply: str


@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request) -> HTMLResponse:
    """Serves the main frontend index.html template."""
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request})


@app.post("/api/mcq-submit", response_model=MCQResponse)
async def submit_mcq(request_data: MCQRequest) -> MCQResponse:
    """Analyzes MCQ answers to determine initial mood and get Maa's reaction."""
    mood, maa_initial_message = await analyze_mcq_results(request_data.answers)
    return MCQResponse(mood=mood, maa_initial_message=maa_initial_message)


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request_data: ChatRequest) -> ChatResponse:
    """Chats with the user as Maa, maintaining emotional context."""
    reply = await chat_with_maa(request_data.message, request_data.context, request_data.history)
    return ChatResponse(reply=reply)
