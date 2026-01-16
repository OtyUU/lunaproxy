from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
import httpx
from config import settings
from context_builder import ContextBuilder
from shared import cache, summary_manager
import asyncio

router = APIRouter()

context_builder = ContextBuilder(cache, summary_manager)
client = httpx.AsyncClient(base_url=settings.LLM_BASE_URL)

@router.post("/v1/chat/completions")
async def chat_proxy(request: Request):
    body = await request.json()
    
    # Inject context
    if "messages" in body:
        context_str = context_builder.build()
        for message in body["messages"]:
            if "content" in message and isinstance(message["content"], str):
                if settings.CONTEXT_PLACEHOLDER in message["content"]:
                    message["content"] = message["content"].replace(
                        settings.CONTEXT_PLACEHOLDER, context_str
                    )

    # Forward request
    headers = dict(request.headers)
    # Remove host header to avoid issues with target
    headers.pop("host", None)
    # Ensure API key is set correctly
    headers["authorization"] = f"Bearer {settings.LLM_API_KEY}"
    
    # Handle streaming
    if body.get("stream", False):
        return await handle_streaming(body, headers)
    else:
        return await handle_blocking(body, headers)

async def handle_blocking(body, headers):
    try:
        response = await client.post(
            "/chat/completions",
            json=body,
            headers=headers,
            timeout=60.0
        )
        # Check for summary generation after a successful translation
        asyncio.create_task(check_summary_trigger())
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def handle_streaming(body, headers):
    async def stream_generator():
        async with client.stream(
            "POST",
            "/chat/completions",
            json=body,
            headers=headers,
            timeout=60.0
        ) as response:
            async for chunk in response.aiter_bytes():
                yield chunk
        # Check for summary generation after stream ends
        asyncio.create_task(check_summary_trigger())

    return StreamingResponse(stream_generator(), media_type="text/event-stream")

async def check_summary_trigger():
    total_lines = cache.get_total_lines()
    if summary_manager.should_generate_summary(total_lines):
        # Use more history for summary generation than for context
        history = cache.get_recent_history(limit=settings.SUMMARY_EVERY_N_LINES)
        await summary_manager.generate_summary(history)
