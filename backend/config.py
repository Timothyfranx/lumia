import os
from dotenv import load_dotenv

# Load local environment variables if present
load_dotenv()

# Portaldot RPC Settings (Falls back to the modern public dev node from the Core Team)
PORTALDOT_RPC = os.getenv("PORTALDOT_RPC", "wss://drip-backend-production-8d86.up.railway.app/node")

# Standard Local Substrate Contracts Node RPC (API v9+ fallback for local testing)
LOCAL_CONTRACTS_RPC = os.getenv("LOCAL_CONTRACTS_RPC", "ws://127.0.0.1:9944")

# Port settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
