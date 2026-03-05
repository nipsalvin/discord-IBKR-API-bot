"""
IBKR API Module - Phase 3
Handles connection to Interactive Brokers and trade execution
"""

from dataclasses import dataclass
from typing import Optional, Tuple
from enum import Enum
import config
from ib_insync import IB


class OrderType(Enum):
    """Order types supported by IBKR"""
    MARKET = "MKT"
    LIMIT = "LMT"
    STOP = "STP"
    STOP_LIMIT = "STP LMT"


class OrderAction(Enum):
    """Order actions (BUY or SELL)"""
    BUY = "BUY"
    SELL = "SELL"


@dataclass
class IBKROrder:
    """Represents an IBKR order"""
    symbol: str
    quantity: int
    action: OrderAction
    order_type: OrderType = OrderType.MARKET
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    
    def __str__(self):
        return f"{self.action.value} {self.quantity} {self.symbol} @ {self.order_type.value}"


class IBKRConnection:
    """Manages connection to Interactive Brokers using ib_insync"""

    def __init__(self, host: Optional[str] = None, port: Optional[str] = None, client_id: Optional[str] = None):
        """
        Initialize IBKR connection parameters

        Args:
            host: IBKR Gateway/TWS host (default from config)
            port: IBKR Gateway/TWS port (default from config)
            client_id: Client ID for connection (default from config)
        """
        self.host = host or config.IBKR_HOST
        self.port = int(port or config.IBKR_PORT)
        self.client_id = int(client_id or config.IBKR_CLIENT_ID)
        self.ib = IB()
        self.next_order_id = None
        
    def connect(self) -> Tuple[bool, str]:
        """
        Connect to IBKR Gateway/TWS

        Returns:
            Tuple of (success, message)
        """
        try:
            print(f"🔌 Attempting to connect to IBKR at {self.host}:{self.port}")

            # Connect to IBKR
            self.ib.connect(self.host, self.port, clientId=self.client_id)

            message = f"✅ Connected to IBKR at {self.host}:{self.port}"
            print(message)
            return True, message

        except Exception as e:
            error_msg = f"Failed to connect to IBKR: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def disconnect(self) -> Tuple[bool, str]:
        """
        Disconnect from IBKR

        Returns:
            Tuple of (success, message)
        """
        try:
            if self.ib.isConnected():
                self.ib.disconnect()
                return True, "Disconnected from IBKR"
            return True, "Already disconnected"

        except Exception as e:
            error_msg = f"Error disconnecting from IBKR: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def is_ready(self) -> bool:
        """Check if connection is ready for trading"""
        return self.ib.isConnected()
    
    def place_order(self, order: IBKROrder) -> Tuple[bool, str, Optional[int]]:
        """
        Place an order on IBKR

        Args:
            order: IBKROrder object with order details

        Returns:
            Tuple of (success, message, order_id)
        """
        if not self.ib.isConnected():
            return False, "Not connected to IBKR", None
        
        try:
            # TODO: Implement actual order placement using ibapi
            # This should:
            # 1. Create a contract object
            # 2. Create an order objectTesting market data req
            # 3. Place the order via EClient
            # 4. Return the order ID
            
            order_id = 1  # Placeholder
            message = f"Order placed: {order}"
            print(f"✅ {message}")
            return True, message, order_id
            
        except Exception as e:
            error_msg = f"Failed to place order: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg, None
    
    def cancel_order(self, order_id: int) -> Tuple[bool, str]:
        """
        Cancel an order

        Args:
            order_id: The order ID to cancel

        Returns:
            Tuple of (success, message)
        """
        if not self.ib.isConnected():
            return False, "Not connected to IBKR"
        
        try:
            # TODO: Implement actual order cancellation
            message = f"Order {order_id} cancelled"
            print(f"✅ {message}")
            return True, message
            
        except Exception as e:
            error_msg = f"Failed to cancel order: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def get_account_summary(self) -> Tuple[bool, dict]:
        """
        Get account summary information

        Returns:
            Tuple of (success, account_data)
        """
        if not self.ib.isConnected():
            return False, {}
        
        try:
            # TODO: Implement account summary retrieval
            account_data = {
                "buying_power": 0.0,
                "cash": 0.0,
                "portfolio_value": 0.0,
            }
            return True, account_data
            
        except Exception as e:
            print(f"❌ Failed to get account summary: {str(e)}")
            return False, {}


class IBKRTradeExecutor:
    """High-level interface for executing trades from signals"""

    def __init__(self, connection: Optional[IBKRConnection] = None):
        """
        Initialize trade executor
        
        Args:
            connection: IBKRConnection instance (creates new if not provided)
        """
        self.connection = connection or IBKRConnection()
    
    def execute_signal(self, signal) -> Tuple[bool, str, Optional[int]]:
        """
        Execute a trade based on a TradingSignal
        
        Args:
            signal: TradingSignal object from signal_parser
            
        Returns:
            Tuple of (success, message, order_id)
        """
        if not self.connection.is_ready():
            return False, "IBKR connection not ready", None
        
        try:
            # TODO: Convert TradingSignal to IBKROrder
            # This should handle:
            # 1. Determining if it's a BUY or SELL based on action
            # 2. Creating appropriate contract for options
            # 3. Setting quantity from signal
            
            message = f"Signal execution not yet implemented for {signal.instrument}"
            print(f"⚠️  {message}")
            return False, message, None
            
        except Exception as e:
            error_msg = f"Error executing signal: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg, None

