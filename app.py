import os
import re
from telethon import TelegramClient, events
import asyncio
from aiohttp import web

# Retrieve API credentials from environment variables
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')
phone_number = os.getenv('TELEGRAM_PHONE')

# Initialize the Telegram client using the session file
client = TelegramClient('my_session', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    chat_id = event.chat_id
    message_text = event.raw_text
    print(f"Received message from chat {chat_id}: {message_text}")

    # Define a regex pattern to match the code
    code_pattern = r'[A-Za-z0-9]{8}'  # 8-character alphanumeric string

    if chat_id == -1002157712325:
        print("Message is from the source chat. Checking for code...")
        match = re.search(code_pattern, message_text)
        if match:
            code = match.group(0)
            print(f"Code found: {code}")
            formatted_code = f"`{code}`"
            print(f"Forwarding code: {formatted_code}")
            await client.send_message(-4510674591, formatted_code)
            print(f"Code forwarded to target chat: {formatted_code}")
        else:
            print("No code found in the message.")
    else:
        print(f"Message received from unexpected chat {chat_id}.")

# Start the Telegram client
async def start_telegram_client():
    await client.start()
    await client.run_until_disconnected()

# Dummy HTTP server handler
async def handle(request):
    return web.Response(text="The Telegram bot is running!")

# Start the web app and Telegram client
async def init_app():
    asyncio.create_task(start_telegram_client())
    app = web.Application()
    app.router.add_get('/', handle)
    return app

# Main entry point
if __name__ == '__main__':
    web.run_app(init_app(), port=10000)
