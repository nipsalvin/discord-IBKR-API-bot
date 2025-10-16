"""
Signal Parser Module - Phase 2
Parses trading signals from Discord messages
"""

import re
from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class TradingSignal:
    """Represents a parsed trading signal"""
    instrument: str
    strike: float
    option_type: str  # 'CALL' or 'PUT'
    quantity: Optional[int] = None
    action: Optional[str] = None  # 'BUY', 'SELL', 'TAKE', etc.
    raw_message: str = ""

    def __str__(self):
        return f"{self.action or 'TRADE'} {self.quantity or 1}x {self.instrument} {self.strike}{self.option_type[0]} ({self.option_type})"


class SignalParser:
    """Parses trading signals from Discord messages"""

    # Common option type abbreviations
    OPTION_TYPES = {
        'C': 'CALL',
        'CALL': 'CALL',
        'P': 'PUT',
        'PUT': 'PUT',
    }

    # Common action words (ordered by length, longest first to avoid substring matches)
    ACTIONS = [
        'taking', 'buying', 'selling', 'opening', 'closing', 'exiting',
        'take', 'buy', 'sell', 'open', 'close', 'exit'
    ]

    @staticmethod
    def parse(message: str) -> Optional[TradingSignal]:
        """
        Parse a trading signal from a message.
        
        Examples:
            "I'm taking SPY 670P" -> SPY 670 PUT
            "buying 5x QQQ 400C" -> QQQ 400 CALL (qty: 5)
            "SPX 5000P" -> SPX 5000 PUT
        
        Args:
            message: The Discord message content
            
        Returns:
            TradingSignal object if parsed successfully, None otherwise
        """
        message_lower = message.lower()
        original_message = message
        
        # Pattern: [action] [quantity]x [SYMBOL] [STRIKE][C/P]
        # Using word boundaries and case-insensitive matching
        pattern = r'(?:taking|buying|selling|opening|closing|exiting|take|buy|sell|open|close|exit)?\s*(?:(\d+)x?)?\s*([a-zA-Z]{1,5})\s+(\d+(?:\.\d+)?)\s*([cpCP])'
        
        match = re.search(pattern, message, re.IGNORECASE)
        
        if not match:
            return None
        
        quantity_str, symbol, strike_str, option_type_char = match.groups()
        
        # Extract action from message
        action = None
        for act in SignalParser.ACTIONS:
            if act in message_lower:
                action = act.upper()
                break
        
        # Parse option type
        option_type = SignalParser.OPTION_TYPES.get(option_type_char.upper())
        if not option_type:
            return None
        
        # Parse quantity
        quantity = int(quantity_str) if quantity_str else None
        
        # Parse strike
        try:
            strike = float(strike_str)
        except ValueError:
            return None
        
        return TradingSignal(
            instrument=symbol.upper(),
            strike=strike,
            option_type=option_type,
            quantity=quantity,
            action=action,
            raw_message=original_message
        )

    @staticmethod
    def validate_signal(signal: TradingSignal) -> Tuple[bool, str]:
        """
        Validate a parsed signal.
        
        Args:
            signal: The TradingSignal to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not signal.instrument:
            return False, "Invalid instrument symbol"
        
        if len(signal.instrument) > 5:
            return False, "Instrument symbol too long (max 5 characters)"
        
        if signal.strike <= 0:
            return False, "Strike price must be positive"
        
        if signal.option_type not in ['CALL', 'PUT']:
            return False, "Option type must be CALL or PUT"
        
        if signal.quantity and signal.quantity <= 0:
            return False, "Quantity must be positive"
        
        # Reasonable strike price validation (optional)
        if signal.strike >= 100000:
            return False, "Strike price seems unreasonably high"
        
        return True, ""