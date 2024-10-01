import re
from telethon import TelegramClient, events

api_id = 28607871
api_hash = '183721dca18fce6ed2877fdcd1066a3a'

# Initialize the Telegram client
client = TelegramClient('anon', api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    chat = await event.get_chat()
    chat_id = event.chat_id
    print("{} {}".format(chat_id, chat))

    # Define a regex pattern to match the code
    code_pattern = r'[A-Za-z0-9]{8}'  # Assuming the code is an 8-character alphanumeric string

    # Check if the message is from the first chat (-1001610472708)
    if chat_id == -1006215913661:
        # Extract the code part from the message using regex
        match = re.search(code_pattern, event.raw_text)
        
        if match:
            # Get the code from the match
            code = match.group(0)

            # Format the code in monospace
            formatted_code = f"`{code}`"  # Enclose the code with backticks for monospace

            # Forward the formatted code to the second chat (-4510674591)
            await client.send_message(-1002171874012, formatted_code)

    # Optionally handle other chats here as needed
    if chat_id == -1002171874012:
        # You can add any logic for handling messages from this chat
        pass

# Start the client and run it until disconnected
client.start()
client.run_until_disconnected()
