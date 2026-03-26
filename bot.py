import traceback
import discord
from discord.ext import commands
import config
from signal_parser import SignalParser
from ibkr_api import IBKRConnection, IBKRTradeExecutor, IBKROrder, OrderAction, OrderType

# Initialize bot with message content intent
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    """Called when bot successfully connects to Discord"""
    print(f'✅ Bot logged in as {bot.user.name} (ID: {bot.user.id})') # pyright: ignore[reportOptionalMemberAccess]
    print(f'📡 Monitoring channel ID: {config.SIGNALS_CHANNEL_ID}')
    print(f'👤 Listening for messages from user ID: {config.BRIDGE_USER_ID}')
    print('🤖 Bot is ready and listening...\n')

@bot.event
async def on_message(message):
    """Called whenever a message is sent in any channel the bot can see"""
    
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Only process messages from the specific channel
    print(f'🔍 Debug: Message channel ID = {message.channel.id}')
    print(f'🔍 Debug: Config channel ID = {config.SIGNALS_CHANNEL_ID}')
    
    if message.channel.id != config.SIGNALS_CHANNEL_ID:
        print(f'⚠️  Ignoring message from different channel')
        return
    
    # Only process messages from the bridge user
    print(f'🔍 Debug: Message author ID = {message.author.id}')
    print(f'🔍 Debug: Config bridge user ID = {config.BRIDGE_USER_ID}')

    if message.author.id != config.BRIDGE_USER_ID:
        print(f'⚠️  Ignoring message from different user ({message.author.name})')
        return
    
    # Log the message for debugging
    print(f'📨 Signal received from {message.author.name}:')
    print(f'   Content: {message.content}')
    print(f'   Timestamp: {message.created_at}\n')

    # Acknowledge receipt (for testing)
    await message.add_reaction('👀')

    # Phase 2: Parse trading signal
    signal = SignalParser.parse(message.content)

    if signal:
        # Validate the signal
        is_valid, error_msg = SignalParser.validate_signal(signal)

        if is_valid:
            print(f'✅ Signal parsed successfully:')
            print(f'   Instrument: {signal.instrument}')
            print(f'   Strike: {signal.strike}')
            print(f'   Type: {signal.option_type}')
            if signal.quantity:
                print(f'   Quantity: {signal.quantity}')
            if signal.action:
                print(f'   Action: {signal.action}')
            print(f'   Summary: {signal}\n')

            # TODO: Execute trade on IBKR (Phase 3)
            try:
                print(f'\n 🚀 Attempting to execute trade on IBKR for signal: {signal}')
                conn = IBKRConnection()
                conn.connect()

                new_order = IBKROrder(
                    symbol=signal.instrument,
                    quantity=signal.quantity or 0,
                    action=OrderAction.BUY if signal.action == 'BUY' else OrderAction.SELL,
                    order_type=OrderType.MARKET
                )
                print(f'🚀 Executing trade on IBKR: {new_order}')

                conn.place_order(new_order)
                conn.disconnect()
            except Exception as e:
                print(f'❌ Error executing trade: {e}')
                traceback.print_exc()
                await message.reply(f'❌ Error executing trade: {str(e)}')
        else:
            print(f'❌ Signal validation failed: {error_msg}\n')
            # This can be used for responding to the user
            await message.reply(f'❌ Invalid signal: {error_msg}')
    else:
        print(f'⚠️  Could not parse trading signal from message\n')
        # This can be used for responding to the user
        await message.reply(f'❌ Could not parse trading signal from message')

    # Process commands (if any are added later)
    await bot.process_commands(message)

@bot.event
async def on_error(event, *args, **kwargs):
    """Handle errors gracefully"""
    print(f'❌ Error in {event}')
    traceback.print_exc()

# Run the bot
if __name__ == '__main__':
    try:
        print('🚀 Starting Discord Trading Bot...')
        bot.run(config.DISCORD_BOT_TOKEN)   # pyright: ignore[reportArgumentType]
    except KeyboardInterrupt:
        print('\n⚠️  Bot stopped by user')
    except Exception as e:
        print(f'❌ Fatal error: {e}')
        traceback.print_exc()
