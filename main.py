from fastapi import FastAPI
import httpx
from dotenv import load_dotenv
import json
import os

load_dotenv()

client_id = os.getenv("SEATGEEK_CLIENT_ID")
app = FastAPI()

# uvicorn main:app --reload 

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/fetch-events/{route}")
async def fetchEvents(route):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.seatgeek.com/2/events/?client_id={client_id}&q={route}&per_page=5&page=1")
        data = response.json()
        return data
