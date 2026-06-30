from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.models import User, Product          # ensures tables register
from app.routers import auth, products

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


@app.get("/")
def health():
    return {"status": "ok"}