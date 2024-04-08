from fastapi import FastAPI
import httpx
from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from contextlib import asynccontextmanager


load_dotenv()

client_id = os.getenv("SEATGEEK_CLIENT_ID")

# uvicorn main:app --reload 
# loads MongoDB before starting the server
# note: asyncio not explicitly necessary as FastAPI already uses asyncio
@asynccontextmanager
async def lifespan(app: FastAPI):
    uri = os.getenv("MONGODB_URI")
    client = AsyncIOMotorClient(uri, server_api=ServerApi("1"))
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
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.seatgeek.com/2/events/?client_id={client_id}&q={route}&per_page=1&page=1")
        data = response.json()
        print(data['events'][0]["venue"]["location"])
        # data['events'][0]["venue"]["location"] is coordinates in dictionary
        # {'lat': 40.7509, 'lon': -73.9943}
        return data
