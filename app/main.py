import uvicorn
import asyncio
from app.models.database import database
from app.routers import users, api, events, notifications, other
from ap.utils import main
from fastapi import FastAPI



#import uvloop
#loop = uvloop.new_event_loop()

class BackgroundRunner:

    async def main(self):
        
        w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/f7b4f0c651b84c2e93b45e1a398f4f6b'))
        abi = open("ohm.json").read()
        abi_tres = open("treasury.json").read()

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

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()
    asyncio.create_task(runner.main())



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
