from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.models import User, Product          # ensures tables register
from app.routers import auth, products
from app.core.cache import cache_ping
from app.routers import auth, products, ai
# Dev convenience: create tables on startup. Phase 4 replaces this with Alembic.
#Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Shopping Copilot API")

# Chrome extensions call from a different origin → CORS must allow it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # tighten to your extension id later
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(ai.router)

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/health/redis")
def redis_health():
    return {"redis_connected": cache_ping()}