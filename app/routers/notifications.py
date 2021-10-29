from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from notifications.bot import dp, bot, TOKEN, change_unstake, change_dao, change_transfer, transfer_dao, change_reserves, change_mint, change_state

router = APIRouter()

class Item(BaseModel):
    amount: int = 1

class Amounts(BaseModel):
    amount_dai: int = -1
    amount_frax: int = -1
    amount_weth: int = -1
    amount_lusd: int = -1

class Roles(BaseModel):
	RESERVEDEPOSITOR:int = 2,
	RESERVESPENDER:int = 2,
	RESERVETOKEN:int = 2,
	RESERVEMANAGER:int = 2,
	LIQUIDITYDEPOSITOR:int = 2,
	LIQUIDITYTOKEN:int = 2,
	LIQUIDITYMANAGER:int = 2,
	DEBTOR:int = 2,
	REWARDMANAGER:int = 2,
	SOHM:int = 2

class States(BaseModel):
    unstake: int = 2
    dao_transfer: int = 2
    transfer: int = 2
    minting: int = 2
    minter_role: int = 2
    treasury_balance: int = 2
    change_role: int = 2


@router.post("/api/change_unstake")
async def handle_change_unstake(item: Item):

    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    fake_db["unstake"] = item.amount

    f = open("notifications.txt",'w')
    f.write(str(fake_db))
    f.close()
    await change_unstake(item.amount)

    return {"data":fake_db}

@router.post("/api/change_mint")
async def handle_change_mint(item: Item):

    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    fake_db["mint"] = item.amount

    f = open("notifications.txt",'w')
    f.write(str(fake_db))
    f.close()
    await change_mint(item.amount)

    return {"data":fake_db}

@router.post("/api/change_reserves")
async def handle_change_unstake(item: Amounts):

    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    if item.amount_dai != -1:
    	fake_db["reserves_dai"] = item.amount_dai
    if item.amount_frax != -1:
    	fake_db["reserves_frax"] = item.amount_frax
    if item.amount_lusd != -1:
    	fake_db["reserves_lusd"] = item.amount_lusd
    if item.amount_weth != -1:
    	fake_db["reserves_weth"] = item.amount_weth

    f = open("notifications.txt",'w')
    f.write(str(fake_db))
    f.close()
    await change_reserves(item.amount_dai, item.amount_frax, item.amount_lusd, item.amount_weth)

    return {"data":fake_db}

@router.post("/api/change_dao_transfer")
async def handle_change_dao(item: Item):

    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    fake_db["dao_transfer"] = item.amount

    f = open("notifications.txt",'w')
    f.write(str(fake_db))
    f.close()
    await change_dao(item.amount)

    return {"data":fake_db}

@router.post("/api/change_large_transfer")
async def handle_change_transfer(item: Item):

    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    fake_db["transfer"] = item.amount

    f = open("notifications.txt",'w')
    f.write(str(fake_db))
    f.close()

    await change_transfer(item.amount)

    return {"data":fake_db}

@router.get("/api/notifications_states")
async def states():
    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    return {"data":fake_db}

@router.post("/api/set_states")
async def states(item: States):
    f = open("notifications.txt")
    fake_db = eval(f.read())
    f.close()

    if item.unstake != 2:
        fake_db['states']["unstake"] = item.unstake
        await change_state("unstakes", item.unstake)
    if item.dao_transfer != 2:
        fake_db['states']["dao_transfer"] = item.dao_transfer
        await change_state("dao transfers", item.dao_transfer)
    if item.transfer != 2:
        fake_db['states']["transfer"] = item.transfer
        await change_state("all transfers", item.transfer)
    if item.minting != 2:
        fake_db['states']["minting"] = item.minting
        await change_state("mintings", item.minting)
    if item.minter_role != 2:
        fake_db['states']["minter_role"] = item.minter_role
        await change_state("minters role changes", item.minter_role)
    if item.treasury_balance != 2:
        fake_db['states']["treasury_balance"] = item.treasury_balance
        await change_state("reserves changes", item.treasury_balance)
    if item.change_role != 2:
        fake_db['states']["change_role"] = item.change_role
        await change_state("roles changes", item.change_role)

    f = open("notifications.txt",'w')
    f.write(str(fake_db))
    f.close()

    return {"data":fake_db}