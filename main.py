from fastapi import FastAPI
import httpx
from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from contextlib import asynccontextmanager
from bson import ObjectId
from EventModel import Event
from MapModel import Map


load_dotenv() # loads environment variables

client_id = os.getenv("SEATGEEK_CLIENT_ID")

# uvicorn main:app --reload 
# loads MongoDB before starting the server
# note: asyncio not explicitly necessary as FastAPI already uses asyncio
@asynccontextmanager
async def lifespan(app: FastAPI):
    uri = os.getenv("MONGODB_URI")
    client = AsyncIOMotorClient(uri, server_api=ServerApi("1"))
    app.state.db = client # attach the client to the app state
    try:
        await client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    yield
    client.close()
    print("Ending")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# route to fetch events based on a specified query
@app.get("/fetch-events/{route}")
async def fetchEvents(route):
    async with httpx.AsyncClient() as client: #  with statement to close the client after the request
        response = await client.get(f"https://api.seatgeek.com/2/events/?client_id={client_id}&q={route}&per_page=5&page=1")
        data = response.json()
        events = [Event(**event) for event in data["events"]]
        return events

@app.get("/fetch-map/{route}")
async def fetchMap(route):
    map_id = route
    db = app.state.db
    try:
        map = await db["maps"].find_one({"id": ObjectId(map_id)})
        if map:
            map["_id"] = str(map["_id"])
            return map # returns json representation of map
        else:
            return {"error": "Map not found"}
    except:
        return {"error": "Unexpected Result"}
    
@app.post("/create-map")
async def createMap(map: Map):
    db = app.state.db
    insert_result = await db["maps"].insert_one(map)
    return insert_result.inserted_id



