import os
import re
import asyncio
from telethon import TelegramClient, events
from aiohttp import web

# Retrieve API credentials from environment variables
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')
phone_number = os.getenv('TELEGRAM_PHONE')

# Initialize the Telegram client
client = TelegramClient('my_session', api_id, api_hash)

# Telegram event handler with debugging
@client.on(events.NewMessage)
async def handler(event):
    chat = await event.get_chat()
    chat_id = event.chat_id
    print(f"Received a message from chat {chat_id}: {event.raw_text}")

    # Define a regex pattern to match the code
    code_pattern = r'[A-Za-z0-9]{8}'  # Assuming the code is an 8-character alphanumeric string

    # Check if the message is from the first chat (-1001610472708)
    if chat_id == -1001610472708:
        print("Message is from the target chat. Checking for the code pattern...")
        
        # Extract the code part from the message using regex
        match = re.search(code_pattern, event.raw_text)
        
        if match:
            # Get the code from the match
            code = match.group(0)
            print(f"Code found: {code}")

            # Format the code in monospace
            formatted_code = f"`{code}`"  # Enclose the code with backticks for monospace

            # Forward the formatted code to the second chat (-1002171874012)
            await client.send_message(-1002171874012, formatted_code)
            print("Code forwarded to the target chat.")
        else:
            print("No code found in the message.")
    else:
        print(f"Message received from chat {chat_id}, not the source chat.")

# Start the Telegram client
async def start_telegram_client():
    await client.start(phone_number=phone_number)
    await client.run_until_disconnected()

# Dummy HTTP server handler
async def handle(request):
    return web.Response(text="The Telegram bot is running!")

# Start the web app and Telegram client
async def init_app():
    # Start the Telegram client in the background
    asyncio.create_task(start_telegram_client())

    # Create a simple web app
    app = web.Application()
    app.router.add_get('/', handle)

    return app

# Main entry point
if __name__ == '__main__':
    # Run the web app on port 10000 (or any other available port)
    web.run_app(init_app(), port=10000)
