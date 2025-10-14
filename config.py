import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord Configuration
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
SIGNALS_CHANNEL_ID = int(os.getenv('MY_CHANNEL_ID'))  # pyright: ignore[reportArgumentType]
BRIDGE_USER_ID = int(os.getenv('TEST_USER_ID')) # pyright: ignore[reportArgumentType]

# IBKR Configuration (for later phases)
IBKR_HOST = os.getenv('IBKR_HOST', '127.0.0.1')
IBKR_PORT = os.getenv('IBKR_PORT', '4002')
IBKR_CLIENT_ID = os.getenv('IBKR_CLIENT_ID', '1')

# Validate required environment variables
if not DISCORD_BOT_TOKEN:
    raise ValueError("DISCORD_BOT_TOKEN not found in .env file")
if not SIGNALS_CHANNEL_ID:
    raise ValueError("SIGNALS_CHANNEL_ID not found in .env file")
if not BRIDGE_USER_ID:
    raise ValueError("BRIDGE_USER_ID not found in .env file")
