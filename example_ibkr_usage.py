"""
Example usage of the IBKR API module with ib_insync

This demonstrates how to:
1. Connect to IBKR
2. Get market data
3. Place orders
4. Disconnect
"""

from ibkr_api import IBKRConnection, IBKROrder, OrderAction, OrderType
from ib_insync import Stock


def example_connect_and_get_market_data():
    """Example: Connect and get market data for a stock"""
    print("=" * 60)
    print("Example 1: Connect and Get Market Data")
    print("=" * 60)
    
    # Create connection
    conn = IBKRConnection()
    
    # Connect to IBKR
    success, message = conn.connect()
    print(f"Connection: {message}")
    
    if success:
        # Get market data for SPY
        contract = Stock('SPY', 'SMART', 'USD')
        ticker = conn.ib.reqMktData(contract)
        
        # Wait for data to fill
        conn.ib.sleep(2)
        
        print(f"SPY Bid: {ticker.bid}")
        print(f"SPY Ask: {ticker.ask}")
        print(f"SPY Last: {ticker.last}")
        
        # Disconnect
        conn.disconnect()
    
    print()


def example_place_market_order():
    """Example: Place a market order"""
    print("=" * 60)
    print("Example 2: Place a Market Order")
    print("=" * 60)
    
    # Create connection
    conn = IBKRConnection()
    
    # Connect to IBKR
    success, message = conn.connect()
    print(f"Connection: {message}")
    
    if success:
        # Create a market buy order for 100 shares of SPY
        order = IBKROrder(
            symbol="SPY",
            quantity=100,
            action=OrderAction.BUY,
            order_type=OrderType.MARKET
        )
        
        # Place the order
        success, message, order_id = conn.place_order(order)
        print(f"Order Result: {message}")
        print(f"Order ID: {order_id}")
        
        # Disconnect
        conn.disconnect()
    
    print()


def example_place_limit_order():
    """Example: Place a limit order"""
    print("=" * 60)
    print("Example 3: Place a Limit Order")
    print("=" * 60)
    
    # Create connection
    conn = IBKRConnection()
    
    # Connect to IBKR
    success, message = conn.connect()
    print(f"Connection: {message}")
    
    if success:
        # Create a limit sell order for 50 shares of QQQ at $350.50
        order = IBKROrder(
            symbol="QQQ",
            quantity=50,
            action=OrderAction.SELL,
            order_type=OrderType.LIMIT,
            limit_price=350.50
        )
        
        # Place the order
        success, message, order_id = conn.place_order(order)
        print(f"Order Result: {message}")
        print(f"Order ID: {order_id}")
        
        # Disconnect
        conn.disconnect()
    
    print()


def example_get_account_summary():
    """Example: Get account summary"""
    print("=" * 60)
    print("Example 4: Get Account Summary")
    print("=" * 60)
    
    # Create connection
    conn = IBKRConnection()
    
    # Connect to IBKR
    success, message = conn.connect()
    print(f"Connection: {message}")
    
    if success:
        # Get account summary
        success, account_data = conn.get_account_summary()
        
        if success:
            print("Account Summary:")
            for key, value in account_data.items():
                print(f"  {key}: {value}")
        else:
            print("Failed to get account summary")
        
        # Disconnect
        conn.disconnect()
    
    print()


if __name__ == '__main__':
    print("\n")
    print("IBKR API Usage Examples")
    print("=" * 60)
    print("Note: These examples require IBKR Gateway/TWS to be running")
    print("      at 127.0.0.1:7497")
    print()
    
    # Uncomment the examples you want to run
    # example_connect_and_get_market_data()
    # example_place_market_order()
    # example_place_limit_order()
    # example_get_account_summary()
    
    print("Examples are commented out to prevent accidental trades.")
    print("Uncomment the function calls above to run them.")

