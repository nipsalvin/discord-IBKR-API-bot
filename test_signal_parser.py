"""
Unit tests for the Signal Parser
"""

import unittest
from signal_parser import SignalParser, TradingSignal


class TestSignalParser(unittest.TestCase):
    """Test cases for signal parsing"""

    def test_basic_put_signal(self):
        """Test parsing 'I'm taking SPY 670P'"""
        message = "Hey guys, I'm taking SPY 670P"
        signal = SignalParser.parse(message)
        
        self.assertIsNotNone(signal)
        self.assertEqual(signal.instrument, "SPY") # type: ignore
        self.assertEqual(signal.strike, 670) # type: ignore
        self.assertEqual(signal.option_type, "PUT") # type: ignore
        self.assertEqual(signal.action, "TAKING") # type: ignore

    def test_basic_call_signal(self):
        """Test parsing 'buying QQQ 400C'"""
        message = "buying QQQ 400C"
        signal = SignalParser.parse(message)
        
        self.assertIsNotNone(signal)
        self.assertEqual(signal.instrument, "QQQ") # type: ignore
        self.assertEqual(signal.strike, 400) # type: ignore
        self.assertEqual(signal.option_type, "CALL") # type: ignore

    def test_signal_with_quantity(self):
        """Test parsing '5x SPX 5000P'"""
        message = "I'm taking 5x SPX 5000P"
        signal = SignalParser.parse(message)
        
        self.assertIsNotNone(signal)
        self.assertEqual(signal.instrument, "SPX") # type: ignore
        self.assertEqual(signal.strike, 5000) # type: ignore
        self.assertEqual(signal.option_type, "PUT") # type: ignore
        self.assertEqual(signal.quantity, 5) # type: ignore

    def test_decimal_strike(self):
        """Test parsing decimal strike prices"""
        message = "selling 2x IWM 210.5C"
        signal = SignalParser.parse(message)
        
        self.assertIsNotNone(signal)
        self.assertEqual(signal.instrument, "IWM") # type: ignore
        self.assertEqual(signal.strike, 210.5) # type: ignore
        self.assertEqual(signal.option_type, "CALL") # type: ignore
        self.assertEqual(signal.quantity, 2) # type: ignore

    def test_invalid_message(self):
        """Test that invalid messages return None"""
        message = "Just some random text"
        signal = SignalParser.parse(message)
        
        self.assertIsNone(signal)

    def test_validation_valid_signal(self):
        """Test validation of a valid signal"""
        signal = TradingSignal(
            instrument="SPY",
            strike=670,
            option_type="PUT"
        )
        
        is_valid, error_msg = SignalParser.validate_signal(signal)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")

    def test_validation_invalid_strike(self):
        """Test validation fails for negative strike"""
        signal = TradingSignal(
            instrument="SPY",
            strike=-100,
            option_type="PUT"
        )
        
        is_valid, error_msg = SignalParser.validate_signal(signal)
        self.assertFalse(is_valid)
        self.assertIn("positive", error_msg.lower())

    def test_validation_invalid_quantity(self):
        """Test validation fails for invalid quantity"""
        signal = TradingSignal(
            instrument="SPY",
            strike=670,
            option_type="PUT",
            quantity=-5
        )
        
        is_valid, error_msg = SignalParser.validate_signal(signal)
        self.assertFalse(is_valid)
        self.assertIn("positive", error_msg.lower())

    def test_signal_string_representation(self):
        """Test the string representation of a signal"""
        signal = TradingSignal(
            instrument="SPY",
            strike=670,
            option_type="PUT",
            quantity=3,
            action="BUYING"
        )
        
        signal_str = str(signal)
        self.assertIn("SPY", signal_str)
        self.assertIn("670", signal_str)
        self.assertIn("PUT", signal_str)
        self.assertIn("3", signal_str)

    def test_case_insensitive_parsing(self):
        """Test that parsing is case insensitive"""
        message = "taking spy 670p"
        signal = SignalParser.parse(message)
        
        self.assertIsNotNone(signal)
        self.assertEqual(signal.instrument, "SPY") # type: ignore
        self.assertEqual(signal.option_type, "PUT") # type: ignore

    def test_multiple_actions(self):
        """Test parsing with different action words"""
        test_cases = [
            ("taking SPY 670P", "TAKING"),
            ("buying QQQ 400C", "BUYING"),
            ("selling IWM 210P", "SELLING"),
            ("opening SPX 5000C", "OPENING"),
            ("closing XLF 35P", "CLOSING"),
        ]

        for message, expected_action in test_cases:
            signal = SignalParser.parse(message)
            self.assertIsNotNone(signal, f"Failed to parse: {message}")
            self.assertEqual(signal.action, expected_action, f"Wrong action for: {message}") # type: ignore


if __name__ == '__main__':
    unittest.main()

