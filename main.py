from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any

from ai_engine import analyze_mcq_results, chat_with_maa, generate_insights

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
    answers: List[str] = Field(..., max_items=5)

class MCQResponse(BaseModel):
    mood: str
    maa_initial_message: str

class ChatRequest(BaseModel):
    message: str = Field(..., max_length=1000)
    context: str = Field(..., max_length=50)
    history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    reply: str

class InsightsRequest(BaseModel):
    history: List[Dict[str, str]]

class InsightsResponse(BaseModel):
    hidden_triggers: List[str]
    cognitive_distortions: List[str]
    emotional_pattern: str
    wellness_score: int
    action_plan: List[str]


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


@app.post("/api/insights", response_model=InsightsResponse)
async def insights(request_data: InsightsRequest) -> InsightsResponse:
    """Analyzes the chat history to uncover hidden stress triggers and emotional patterns."""
    result = await generate_insights(request_data.history)
    return InsightsResponse(**result)
