"""
Unit tests for IBKR API Module
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from ibkr_api import (
    IBKRConnection, IBKROrder, IBKRTradeExecutor,
    OrderType, OrderAction
)


class TestIBKROrder(unittest.TestCase):
    """Test cases for IBKROrder"""
    
    def test_create_market_buy_order(self):
        """Test creating a market buy order"""
        order = IBKROrder(
            symbol="SPY",
            quantity=100,
            action=OrderAction.BUY,
            order_type=OrderType.MARKET
        )
        
        self.assertEqual(order.symbol, "SPY")
        self.assertEqual(order.quantity, 100)
        self.assertEqual(order.action, OrderAction.BUY)
        self.assertEqual(order.order_type, OrderType.MARKET)
    
    def test_create_limit_sell_order(self):
        """Test creating a limit sell order"""
        order = IBKROrder(
            symbol="QQQ",
            quantity=50,
            action=OrderAction.SELL,
            order_type=OrderType.LIMIT,
            limit_price=350.50
        )
        
        self.assertEqual(order.symbol, "QQQ")
        self.assertEqual(order.quantity, 50)
        self.assertEqual(order.action, OrderAction.SELL)
        self.assertEqual(order.order_type, OrderType.LIMIT)
        self.assertEqual(order.limit_price, 350.50)
    
    def test_order_string_representation(self):
        """Test string representation of order"""
        order = IBKROrder(
            symbol="IWM",
            quantity=25,
            action=OrderAction.BUY,
            order_type=OrderType.MARKET
        )
        
        order_str = str(order)
        self.assertIn("BUY", order_str)
        self.assertIn("25", order_str)
        self.assertIn("IWM", order_str)


class TestIBKRConnection(unittest.TestCase):
    """Test cases for IBKRConnection"""

    def test_connection_initialization(self):
        """Test connection initialization with defaults"""
        with patch('ibkr_api.IB'):
            conn = IBKRConnection()

            self.assertEqual(conn.host, "127.0.0.1")
            self.assertEqual(conn.port, 7497)
            self.assertEqual(conn.client_id, 1)

    def test_connection_initialization_with_custom_params(self):
        """Test connection initialization with custom parameters"""
        with patch('ibkr_api.IB'):
            conn = IBKRConnection(
                host="192.168.1.100",
                port="7498",
                client_id="2"
            )

            self.assertEqual(conn.host, "192.168.1.100")
            self.assertEqual(conn.port, 7498)
            self.assertEqual(conn.client_id, 2)

    def test_connect_success(self):
        """Test successful connection"""
        with patch('ibkr_api.IB') as mock_ib:
            mock_instance = MagicMock()
            mock_ib.return_value = mock_instance

            conn = IBKRConnection()
            success, message = conn.connect()

            self.assertTrue(success)
            self.assertIn("Connected", message)
            mock_instance.connect.assert_called_once()

    def test_disconnect_success(self):
        """Test successful disconnection"""
        with patch('ibkr_api.IB') as mock_ib:
            mock_instance = MagicMock()
            mock_ib.return_value = mock_instance
            mock_instance.isConnected.return_value = True

            conn = IBKRConnection()
            success, message = conn.disconnect()

            self.assertTrue(success)
            self.assertIn("Disconnected", message)
            mock_instance.disconnect.assert_called_once()

    def test_disconnect_when_not_connected(self):
        """Test disconnecting when not connected"""
        with patch('ibkr_api.IB') as mock_ib:
            mock_instance = MagicMock()
            mock_ib.return_value = mock_instance
            mock_instance.isConnected.return_value = False

            conn = IBKRConnection()
            success, message = conn.disconnect()

            self.assertTrue(success)
            self.assertIn("Already disconnected", message)

    def test_is_ready_when_connected(self):
        """Test is_ready returns True when connected"""
        with patch('ibkr_api.IB') as mock_ib:
            mock_instance = MagicMock()
            mock_ib.return_value = mock_instance
            mock_instance.isConnected.return_value = True

            conn = IBKRConnection()
            self.assertTrue(conn.is_ready())

    def test_is_ready_when_not_connected(self):
        """Test is_ready returns False when not connected"""
        with patch('ibkr_api.IB') as mock_ib:
            mock_instance = MagicMock()
            mock_ib.return_value = mock_instance
            mock_instance.isConnected.return_value = False

            conn = IBKRConnection()
            self.assertFalse(conn.is_ready())
    
    def test_place_order_when_not_connected(self):
        """Test placing order when not connected"""
        with patch('ibkr_api.IB') as mock_ib:
            mock_instance = MagicMock()
            mock_ib.return_value = mock_instance
            mock_instance.isConnected.return_value = False

            conn = IBKRConnection()
            order = IBKROrder(
                symbol="SPY",
                quantity=100,
                action=OrderAction.BUY
            )

            success, message, order_id = conn.place_order(order)

            self.assertFalse(success)
            self.assertIn("Not connected", message)
            self.assertIsNone(order_id)

    def test_place_order_when_connected(self):
        """Test placing order when connected"""
        with patch('ibkr_api.IB') as mock_ib:
            mock_instance = MagicMock()
            mock_ib.return_value = mock_instance
            mock_instance.isConnected.return_value = True

            conn = IBKRConnection()
            order = IBKROrder(
                symbol="SPY",
                quantity=100,
                action=OrderAction.BUY
            )

            success, message, order_id = conn.place_order(order)

            self.assertTrue(success)
            self.assertIsNotNone(order_id)

    def test_cancel_order_when_not_connected(self):
        """Test canceling order when not connected"""
        with patch('ibkr_api.IB') as mock_ib:
            mock_instance = MagicMock()
            mock_ib.return_value = mock_instance
            mock_instance.isConnected.return_value = False

            conn = IBKRConnection()
            success, message = conn.cancel_order(1)

            self.assertFalse(success)
            self.assertIn("Not connected", message)

    def test_cancel_order_when_connected(self):
        """Test canceling order when connected"""
        with patch('ibkr_api.IB') as mock_ib:
            mock_instance = MagicMock()
            mock_ib.return_value = mock_instance
            mock_instance.isConnected.return_value = True

            conn = IBKRConnection()
            success, message = conn.cancel_order(1)

            self.assertTrue(success)
            self.assertIn("cancelled", message)

    def test_get_account_summary_when_not_connected(self):
        """Test getting account summary when not connected"""
        with patch('ibkr_api.IB') as mock_ib:
            mock_instance = MagicMock()
            mock_ib.return_value = mock_instance
            mock_instance.isConnected.return_value = False

            conn = IBKRConnection()
            success, data = conn.get_account_summary()

            self.assertFalse(success)
            self.assertEqual(data, {})

    def test_get_account_summary_when_connected(self):
        """Test getting account summary when connected"""
        with patch('ibkr_api.IB') as mock_ib:
            mock_instance = MagicMock()
            mock_ib.return_value = mock_instance
            mock_instance.isConnected.return_value = True

            conn = IBKRConnection()
            success, data = conn.get_account_summary()

            self.assertTrue(success)
            self.assertIn("buying_power", data)
            self.assertIn("cash", data)
            self.assertIn("portfolio_value", data)


class TestIBKRTradeExecutor(unittest.TestCase):
    """Test cases for IBKRTradeExecutor"""

    def test_executor_initialization_with_default_connection(self):
        """Test executor initialization with default connection"""
        with patch('ibkr_api.IB'):
            executor = IBKRTradeExecutor()

            self.assertIsNotNone(executor.connection)
            self.assertIsInstance(executor.connection, IBKRConnection)

    def test_executor_initialization_with_custom_connection(self):
        """Test executor initialization with custom connection"""
        with patch('ibkr_api.IB'):
            conn = IBKRConnection()
            executor = IBKRTradeExecutor(connection=conn)

            self.assertEqual(executor.connection, conn)

    def test_execute_signal_when_not_connected(self):
        """Test executing signal when not connected"""
        from signal_parser import TradingSignal

        with patch('ibkr_api.IB') as mock_ib:
            mock_instance = MagicMock()
            mock_ib.return_value = mock_instance
            mock_instance.isConnected.return_value = False

            executor = IBKRTradeExecutor()
            signal = TradingSignal(
                instrument="SPY",
                strike=670,
                option_type="PUT"
            )

            success, message, order_id = executor.execute_signal(signal)

            self.assertFalse(success)
            self.assertIn("not ready", message.lower())
            self.assertIsNone(order_id)


if __name__ == '__main__':
    unittest.main()

