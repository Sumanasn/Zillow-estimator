import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import ZillowAutonomousAgent
from dotenv import load_dotenv

# 1. Load from .env if it exists (for local development)
# Docker will ignore this if the file isn't copied, which is fine
load_dotenv()

app = FastAPI()

# 2. Securely fetch the key
# We use os.environ.get to prioritize the Docker injected variable
API_KEY = os.environ.get("ZENROWS_API_KEY")

# 3. Fail-Fast Logic
# If the key is missing, the container will crash immediately with a clear log
if not API_KEY:
    print("--- DEBUG INFO ---")
    print(f"Current Directory: {os.getcwd()}")
    print(f"Available Env Vars: {list(os.environ.keys())}")
    raise ValueError("CRITICAL ERROR: ZENROWS_API_KEY is missing. Check your .env or Docker config.")

# Initialize Agent
agent = ZillowAutonomousAgent(api_key=API_KEY)

class AddressQuery(BaseModel):
    address: str

# 4. Added a Health Check Route
# This is what Docker uses to see if the backend is 'Healthy'
@app.get("/health")
async def health_check():
    return {"status": "online", "agent_initialized": agent is not None}

@app.post("/agent/execute")
async def execute_agent(query: AddressQuery):
    try:
        result = agent.run(query.address)
        if result["status"] == "failed":
            raise HTTPException(status_code=502, detail=result["error"])
        return result
    except Exception as e:
        # Catching unexpected crashes to keep the server alive
        raise HTTPException(status_code=500, detail=str(e))