import uvicorn
import asyncio
from notifications.bot import dp, bot, TOKEN
from aiogram import Dispatcher, Bot, types
from fastapi.middleware.cors import CORSMiddleware
from app.models.database import database
from app.routers import users, api, events, notifications, other
from app.utils.events import log_loop
from fastapi import FastAPI
import asyncio
from web3 import Web3
from threading import Thread
import time
import requests


WEBHOOK_PATH = f"/bot/{TOKEN}/"
WEBHOOK_URL = "https://7973-178-132-207-251.ngrok.io" + WEBHOOK_PATH

#import uvloop
#loop = uvloop.new_event_loop()
'''
class BackgroundRunner:

    async def main(self):

        w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/f7b4f0c651b84c2e93b45e1a398f4f6b'))
        abi = open("./notifications/loops/ohm.json").read()
        abi_tres = open("./notifications/loops/treasury.json").read()

        address = '0x383518188c0c6d7730d91b2c03a03c837814a899'
        contract_instance = w3.eth.contract(address=Web3.toChecksumAddress(address), abi=abi)
        transfer_filter = contract_instance.events.Transfer.createFilter(fromBlock=12525281)
        address_tres = '0x31F8Cc382c9898b273eff4e0b7626a6987C846E8'
        contract_tres = w3.eth.contract(address=address_tres, abi=abi_tres)

        change_queued_filter = contract_tres.events.ChangeQueued.createFilter(fromBlock=12525281) #12525281 for get_all_entries
        reserves_managed_filter = contract_tres.events.ReservesManaged.createFilter(fromBlock=12525281) #12525281
        change_activated_filter = contract_tres.events.ChangeActivated.createFilter(fromBlock=12525281) #12525281


        worker = [Thread(target=log_loop, args=(transfer_filter, 1), daemon=True),
        Thread(target=log_loop, args=(change_activated_filter, 1), daemon=True),
        Thread(target=log_loop, args=(change_queued_filter, 1), daemon=True),
        Thread(target=log_loop, args=(reserves_managed_filter, 1), daemon=True)]

        for item in worker:
            item.start()
       
        while True:
            time.sleep(20)


runner = BackgroundRunner()
'''
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()
    #asyncio.create_task(runner.main())
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )

@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)

@app.get("/twitter/get_id")
async def get_user_id(usernames: str=""):
    headers = {"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAAMBVQEAAAAAM53SnmlTm5qvzqacgc2W0aPuyUQ%3D4VjOnXdLv99M3Jx3r6WZn3UtWoTr3CMLGQecA3Irt8sLlpGIkn"}
    response  = requests.get(f"https://api.twitter.com/2/users/by?usernames={usernames}", headers=headers).json()
    return response

@app.get("/twitter/get_tweets")
async def get_user_id(uid: str = ""):
    headers = {"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAAMBVQEAAAAAM53SnmlTm5qvzqacgc2W0aPuyUQ%3D4VjOnXdLv99M3Jx3r6WZn3UtWoTr3CMLGQecA3Irt8sLlpGIkn"}
    response  = requests.get(f"https://api.twitter.com/2/users/{uid}/tweets?max_results=25&expansions=author_id&user.fields=username,id,name,created_at,profile_image_url&tweet.fields=id,text,created_at", headers=headers).json()
    return response



@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(notifications.router)
app.include_router(events.router)
app.include_router(api.router)
app.include_router(users.router)
app.include_router(other.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
