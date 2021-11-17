import uvicorn
from app.models.database import database
from app.routers import users, api, events, notifications, other
from fastapi import FastAPI

#import uvloop
#loop = uvloop.new_event_loop()

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


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
