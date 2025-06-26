from fastapi import FastAPI, APIRouter, Path, Body
from .core import Core

router = APIRouter(prefix="/pump")

@router.post("/{pid}/price")
def set_price(pid: int = Path(..., ge=1),
              price1: float = Body(...),
              price9: float = Body(...)):
    Core.price(pid, price1, price9)
    return {"ok": True}

@router.post("/{pid}/authorize")
def start(pid: int = Path(..., ge=1), liters: float = Body(...)):
    Core.authorize(pid, liters)
    return {"ok": True}

@router.post("/{pid}/stop")
def stop(pid: int = Path(..., ge=1)):
    Core.stop(pid); return {"ok": True}

@router.post("/{pid}/reset")
def reset(pid: int = Path(..., ge=1)):
    Core.reset(pid); return {"ok": True}

app = FastAPI()
app.include_router(router)
