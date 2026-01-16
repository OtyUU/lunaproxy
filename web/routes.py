from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from config import settings
from shared import cache, summary_manager

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")

@router.get("/ui", response_class=HTMLResponse)
async def index(request: Request):
    history = cache.get_recent_history(limit=20)
    state = summary_manager.state
    return templates.TemplateResponse("index.html", {
        "request": request,
        "history": history,
        "summary": state.get("summary", ""),
        "notes": state.get("notes", ""),
        "settings": settings
    })

@router.post("/ui/notes")
async def update_notes(notes: str = Form(...)):
    summary_manager.update_notes(notes)
    return RedirectResponse(url="/ui", status_code=303)

@router.post("/ui/summary")
async def update_summary(summary: str = Form(...)):
    summary_manager.update_summary(summary)
    return RedirectResponse(url="/ui", status_code=303)

@router.post("/ui/trigger-summary")
async def trigger_summary():
    history = cache.get_recent_history(limit=settings.SUMMARY_EVERY_N_LINES)
    await summary_manager.generate_summary(history)
    return RedirectResponse(url="/ui", status_code=303)
