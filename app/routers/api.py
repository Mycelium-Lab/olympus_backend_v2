from app.schemas import users
from app.utils import users as users_utils
from app.utils.dependencies import get_current_user, check_if_exists
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.scripts.getTop import getTopBalances
from app.scripts.getBalance import getBalances
from app.scripts.firstN import getFirstLegacy
from app.scripts.getTotal import totalWallets, totalBalances

from fastapi.security import OAuth2PasswordBearer
from app.utils import users as users_utils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

router = APIRouter()

'''
this version has no middleware

if u want to use auth, add "current_user: users.User = Depends(get_current_user)" to the routes methods

for example:

    @router.get("/api/get_top_days/")
    async def get_top_days(start: int = 1617291702, days: int = 1, amount: int = 10000, current_user: users.User = Depends(get_current_user)):

        if not current_user:
            return {"data": "invalid token"}

        response  = await getTopBalances(start, days, amount)
        return {"data":response}


'''

@router.get("/test/start_bot")
async def bot_startup(chid: int = 1000000000):
    db_user = await users_utils.get_bot_user_by_chat(chat_id=message.from_user.id)
    if not db_user:
        users_utils.create_bot_user(message.from_user.id, "all")
    return db_user

@router.get("/test/all_users")
async def all_users():
    db_user = users_utils.get_all_bot_users()
    print(db_user)
    return db_user

@router.get("/api/get_top_days/")
async def get_top_days(start: int = 1617291702, days: int = 1, amount: int = 10000):

    response  = await getTopBalances(start, days, amount)
    return {"data":response}

@router.get("/api/get_transfer_from/")
async def get_transfer_from(start: int = 1617291702, days: int = 1):

    response  = await getTransfer(start, days)
    return {"data":response}

@router.get("/api/get_transfer_to/")
async def get_transfer_to(start: int = 1617291702, days: int = 1):

    response  = await getTransferTo(start, days)
    return {"data":response}

@router.get("/api/get_dao_days/")
async def get_dao_days(start: int = 1617291702, days: int = 1):
    wallet = "0x245cc372C84B3645Bf0Ffe6538620B04a217988B"
    response  = await getBalances(start, days, wallet)
    return {"data":response}

@router.get("/api/get_total_wallets/")
async def get_total_wallets(start: int = 1617291702, days: int = 1):
    response  = await totalWallets(start, days)
    return {"data":response}

@router.get("/api/get_total_balances/")
async def get_total_balances(start: int = 1617291702, days: int = 1):
    response  = await totalBalances(start, days)
    return {"data":response}

@router.get("/api/get_first_n/")
async def get_first_n(start: int = 1617291702, days: int = 1, count: int = 1):

    response  = await getFirstLegacy(start, days, count)
    return {"data":response}