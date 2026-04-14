import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import ZillowAutonomousAgent
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

app = FastAPI()

# Retrieve the key securely
API_KEY = os.getenv("ZENROWS_API_KEY")

if not API_KEY:
    raise ValueError("CRITICAL: ZENROWS_API_KEY not found in environment!")

# Initialize Agent with the secure key
agent = ZillowAutonomousAgent(api_key=API_KEY)

class AddressQuery(BaseModel):
    address: str

@app.post("/agent/execute")
async def execute_agent(query: AddressQuery):
    result = agent.run(query.address)
    if result["status"] == "failed":
        raise HTTPException(status_code=502, detail=result["error"])
    return result