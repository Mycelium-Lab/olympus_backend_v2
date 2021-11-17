from app.scripts.indexes import parseNDays, parseNHours, parseNMinutes
from app.scripts.general import parseGANDays, parseGANHours, parseGANMinutes
from app.scripts.rebases import rebaseTimestamps

from app.schemas import users
from app.utils import users as users_utils
from app.utils.dependencies import get_current_user, check_if_exists
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import FastAPI, APIRouter

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

router = APIRouter()

# NEW CODE
@app.get("/api/get_index_n_days")
async def get_indexes_n_days(start: int = 1617291702, end: int = 1636458860, n: int = 1):
    response  = await parseNDays(start, end, n)
    return {"data":response}

@app.get("/api/get_index_n_hours")
async def get_index_n_hours(start: int = 1623700800, end: int = 1623906000, n: int = 1):
    response  = await parseNHours(start, end, n)
    return {"data":response}

@app.get("/api/get_ga_n_minutes")
async def get_index_n_minutes(start: int = 1623702000, end: int = 1623907200, n: int = 1, types: str = 'marketCapacity'):
    response  = await parseGANMinutes(start, end, n, types)
    return {"data":response}

@app.get("/api/get_ga_n_days")
async def get_indexes_n_days(start: int = 1617291702, end: int = 1636458860, n: int = 1, types: str = 'marketCapacity'):
    response  = await parseGANDays(start, end, n, types)
    return {"data":response}

@app.get("/api/get_ga_n_hours")
async def get_index_n_hours(start: int = 1623700800, end: int = 1623906000, n: int = 1, types: str = 'marketCapacity'):
    response  = await parseGANHours(start, end, n, types)
    return {"data":response}

@app.get("/api/get_index_n_minutes")
async def get_index_n_minutes(start: int = 1623702000, end: int = 1623907200, n: int = 1):
    response  = await parseNMinutes(start, end, n)
    return {"data":response}

@app.get("/api/get_rebase_timestamps")
async def get_rebase_timestamps(start: int = 1617291702, end: int = 1636458860):
    response  = await rebaseTimestamps(start, end)
    return {"data":response}

