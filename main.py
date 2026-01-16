from fastapi import FastAPI
from proxy import router as proxy_router, client as proxy_client
from web.routes import router as ui_router
from config import settings
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await proxy_client.aclose()

app = FastAPI(lifespan=lifespan)

# Include UI routes
app.include_router(ui_router)
# Include Proxy routes
app.include_router(proxy_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PROXY_PORT)
