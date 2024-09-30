import os
import re
from telethon import TelegramClient, events

# Retrieve API credentials from environment variables
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')  # Use the bot token if available

# Initialize the Telegram client using the bot token (avoids needing a phone number)
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage)
async def handler(event):
    chat = await event.get_chat()
    chat_id = event.chat_id
    print("{} {}".format(chat_id, chat))

    # Define a regex pattern to match the code
    code_pattern = r'[A-Za-z0-9]{8}'  # Assuming the code is an 8-character alphanumeric string

    # Check if the message is from the first chat (-1001610472708)
    if chat_id == -1001610472708:
        match = re.search(code_pattern, event.raw_text)
        
        if match:
            code = match.group(0)
            formatted_code = f"`{code}`"
            await client.send_message(-1002171874012, formatted_code)

client.run_until_disconnected()
