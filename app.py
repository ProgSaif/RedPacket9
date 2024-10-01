import re
from telethon import TelegramClient, events

api_id = 
api_hash = ''

# Initialize the Telegram client
client = TelegramClient('anon', api_id, api_hash)

# Define the 'from' and 'to' chat channels (support for multiple channels)
from_channels = [-1002439510384]  # List of channels to listen to
to_channels = [-1002171874012]    # List of channels to forward to

# Define a regex pattern to match the code (still looking for 8-character alphanumeric string)
code_pattern = r'[A-Za-z0-9]{8}'

@client.on(events.NewMessage)
async def handler(event):
    chat = await event.get_chat()
    chat_id = event.chat_id

    # Check if the message is from one of the 'from_channels'
    if chat_id in from_channels:
        # Extract the code part from the message using regex
        matches = re.findall(code_pattern, event.raw_text)
        
        if matches:
            # For each code found, send it to all 'to_channels'
            for code in matches:
                # Format the code in monospace
                formatted_code = f"`{code}`"  # Enclose the code with backticks for monospace
                
                # Forward the formatted code to all 'to_channels'
                for to_channel in to_channels:
                    await client.send_message(to_channel, formatted_code)

    # Optionally handle other chats here as needed
    if chat_id in to_channels:
        # You can add any logic for handling messages from the 'to_channels'
        pass

# Start the client and run it until disconnected
client.start()
client.run_until_disconnected()
