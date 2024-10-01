import os
import re
import asyncio
from telethon import TelegramClient, events
from aiohttp import web  # Import for dummy server

# Retrieve API credentials from environment variables
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')
phone_number = os.getenv('TELEGRAM_PHONE')

# Initialize the Telegram client
client = TelegramClient('my_session', api_id, api_hash)

# Telegram event handler
@client.on(events.NewMessage)
async def handler(event):
    chat = await event.get_chat()
    chat_id = event.chat_id
    print("{} {}".format(chat_id, chat))

    # Define a regex pattern to match the code
    code_pattern = r'[A-Za-z0-9]{8}'

    if chat_id == -1001610472708:
        match = re.search(code_pattern, event.raw_text)
        
        if match:
            code = match.group(0)
            formatted_code = f"`{code}`"
            await client.send_message(-1002171874012, formatted_code)

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
