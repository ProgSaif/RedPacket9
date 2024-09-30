import os
import re
from telethon import TelegramClient, events

# Retrieve API credentials from environment variables
api_id = int(os.getenv('TELEGRAM_API_ID'))  # Set this in the Render dashboard
api_hash = os.getenv('TELEGRAM_API_HASH')    # Set this in the Render dashboard
phone_number = os.getenv('TELEGRAM_PHONE')    # Set this in the Render dashboard

# Ensure all necessary environment variables are provided
if not api_id or not api_hash or not phone_number:
    raise ValueError("Missing environment variables. Please set TELEGRAM_API_ID, TELEGRAM_API_HASH, and TELEGRAM_PHONE.")

# Initialize the Telegram client
client = TelegramClient(phone_number, api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    chat = await event.get_chat()
    chat_id = event.chat_id
    print("{} {}".format(chat_id, chat))

    # Define a regex pattern to match the code
    code_pattern = r'[A-Za-z0-9]{8}'  # Assuming the code is an 8-character alphanumeric string

    # Check if the message is from the first chat (-1001610472708)
    if chat_id == -1001610472708:
        # Extract the code part from the message using regex
        match = re.search(code_pattern, event.raw_text)
        
        if match:
            # Get the code from the match
            code = match.group(0)

            # Format the code in monospace
            formatted_code = f"`{code}`"  # Enclose the code with backticks for monospace

            # Forward the formatted code to the second chat (-1002171874012)
            await client.send_message(-1002171874012, formatted_code)

    # Optionally handle other chats here as needed
    if chat_id == -1002171874012:
        pass

# Start the client and run it until disconnected
client.start()
client.run_until_disconnected()
