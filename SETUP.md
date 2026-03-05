# Discord IBKR API Bot - Setup Guide

## Project Overview

A Discord bot that listens for trading signals and executes trades on Interactive Brokers (IBKR).

**Current Phase:** Phase 2 - Trading Signal Parser ✅

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Discord Bot Token
- Discord Channel ID
- Discord User ID (for signal source)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd discord-IBKR-API-bot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
DISCORD_BOT_TOKEN=your_bot_token_here
MY_CHANNEL_ID=your_channel_id_here
TEST_USER_ID=your_user_id_here
IBKR_HOST=127.0.0.1
IBKR_PORT=4002
IBKR_CLIENT_ID=1
```

## Running the Bot

```bash
python bot.py
```

Expected output:
```
🚀 Starting Discord Trading Bot...
✅ Bot logged in as YourBotName (ID: 123456789)
📡 Monitoring channel ID: 987654321
👤 Listening for messages from user ID: 111111111
🤖 Bot is ready and listening...
```

## Running Tests

### Run Signal Parser Tests

```bash
python -m unittest test_signal_parser -v
```

### Run IBKR API Tests

```bash
python -m unittest test_ibkr_api -v
```

### Run All Tests

```bash
python -m unittest discover -v
```

### Run Specific Test

```bash
python -m unittest test_signal_parser.TestSignalParser.test_basic_put_signal -v
```

### Expected Test Output

```
test_basic_call_signal (test_signal_parser.TestSignalParser)
Test parsing 'buying QQQ 400C' ... ok
test_basic_put_signal (test_signal_parser.TestSignalParser)
Test parsing 'I'm taking SPY 670P' ... ok
test_case_insensitive_parsing (test_signal_parser.TestSignalParser)
Test that parsing is case insensitive ... ok
test_decimal_strike (test_signal_parser.TestSignalParser)
Test parsing decimal strike prices ... ok
test_invalid_message (test_signal_parser.TestSignalParser)
Test that invalid messages return None ... ok
test_multiple_actions (test_signal_parser.TestSignalParser)
Test parsing with different action words ... ok
test_signal_string_representation (test_signal_parser.TestSignalParser)
Test the string representation of a signal ... ok
test_signal_with_quantity (test_signal_parser.TestSignalParser)
Test parsing '5x SPX 5000P' ... ok
test_validation_invalid_quantity (test_signal_parser.TestSignalParser)
Test validation fails for invalid quantity ... ok
test_validation_invalid_strike (test_signal_parser.TestSignalParser)
Test validation fails for negative strike ... ok
test_validation_valid_signal (test_signal_parser.TestSignalParser)
Test validation of a valid signal ... ok

----------------------------------------------------------------------
Ran 11 tests in 0.011s

OK
```

## Project Structure

```
discord-IBKR-API-bot/
├── bot.py                      # Main Discord bot
├── config.py                   # Configuration management
├── signal_parser.py            # Phase 2: Signal parsing logic
├── test_signal_parser.py       # Unit tests for signal parser (11 tests)
├── ibkr_api.py                # Phase 3: IBKR connection & trade execution
├── test_ibkr_api.py           # Unit tests for IBKR API (19 tests)
├── example_ibkr_usage.py      # Example usage of IBKR API
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in repo)
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
├── SETUP.md                   # This file
└── venv/                      # Virtual environment
```

## IBKR API Module

The IBKR API module provides classes for connecting to Interactive Brokers using **ib_insync** and executing trades:

### Key Classes

- **IBKRConnection**: Manages connection to IBKR Gateway/TWS
  - `connect()` - Connect to IBKR Gateway/TWS
  - `disconnect()` - Disconnect gracefully
  - `place_order(order)` - Place a trade order
  - `cancel_order(order_id)` - Cancel an order
  - `get_account_summary()` - Get account information
  - `is_ready()` - Check connection status

- **IBKROrder**: Represents a trade order
  - Supports market, limit, stop, and stop-limit orders
  - Configurable quantity, price, and action (BUY/SELL)

- **IBKRTradeExecutor**: High-level interface for executing trades from signals
  - Converts TradingSignal objects to IBKR orders
  - Handles order placement and error handling

### Requirements

- IBKR Gateway or TWS running on `127.0.0.1:7497` (configurable)
- `ib_insync` library (already in requirements.txt)

### Example Usage

```python
from ibkr_api import IBKRConnection, IBKROrder, OrderAction, OrderType
from ib_insync import Stock

# Create connection
conn = IBKRConnection()
success, msg = conn.connect()

if success:
    # Get market data
    contract = Stock('SPY', 'SMART', 'USD')
    ticker = conn.ib.reqMktData(contract)
    conn.ib.sleep(2)
    print(f"SPY Bid: {ticker.bid}")

    # Place a market order
    order = IBKROrder(
        symbol="SPY",
        quantity=100,
        action=OrderAction.BUY,
        order_type=OrderType.MARKET
    )
    success, msg, order_id = conn.place_order(order)

    # Disconnect
    conn.disconnect()
```

### Running Examples

See `example_ibkr_usage.py` for complete examples of:
- Connecting and getting market data
- Placing market orders
- Placing limit orders
- Getting account summary

## Signal Parser Examples

The signal parser recognizes trading signals in various formats:

### Basic Signals

```
"I'm taking SPY 670P"
→ Instrument: SPY, Strike: 670, Type: PUT

"buying QQQ 400C"
→ Instrument: QQQ, Strike: 400, Type: CALL
```

### With Quantity

```
"5x SPX 5000P"
→ Instrument: SPX, Strike: 5000, Type: PUT, Quantity: 5
```

### Decimal Strikes

```
"selling 2x IWM 210.5C"
→ Instrument: IWM, Strike: 210.5, Type: CALL, Quantity: 2
```

### Supported Actions

- taking / take
- buying / buy
- selling / sell
- opening / open
- closing / close
- exiting / exit

## Development Workflow

### Adding New Tests

1. Open `test_signal_parser.py`
2. Add a new test method to `TestSignalParser` class
3. Run tests: `python -m unittest test_signal_parser -v`

### Modifying Signal Parser

1. Edit `signal_parser.py`
2. Run tests to ensure no regressions: `python -m unittest test_signal_parser -v`
3. Update tests if behavior changes

## Troubleshooting

### Bot Won't Start

- Check `.env` file exists and has all required variables
- Verify Discord Bot Token is valid
- Ensure bot has permissions in the Discord server

### Tests Fail

- Verify Python 3.8+ is installed: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt`
- Check for syntax errors in modified files

### Import Errors

- Ensure virtual environment is activated
- Verify all files are in the project root directory
- Check that `signal_parser.py` is in the same directory as `bot.py`

## Next Steps

- **Phase 3:** Implement IBKR trade execution
- **Phase 4:** Add error handling and logging
- **Phase 5:** Add configuration for trade parameters

## Resources

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [IBKR API Documentation](https://interactivebrokers.com/en/trading/ib-api.php)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)

