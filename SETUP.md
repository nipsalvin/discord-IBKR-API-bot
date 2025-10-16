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

### Run All Tests

```bash
python -m unittest test_signal_parser -v
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
├── bot.py                    # Main Discord bot
├── config.py                 # Configuration management
├── signal_parser.py          # Phase 2: Signal parsing logic
├── test_signal_parser.py     # Unit tests for signal parser
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not in repo)
├── .gitignore               # Git ignore rules
├── README.md                # Project documentation
├── SETUP.md                 # This file
└── venv/                    # Virtual environment
```

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

