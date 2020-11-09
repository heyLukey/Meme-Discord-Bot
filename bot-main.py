import discord
import re
from data import calls, token

client = discord.Client()


# Write messages to log file (with relevant information)
def log(msg):
    userMsg = '(' + str(msg.channel) + ' | ' + str(msg.created_at) + ') ' + str(msg.author) + ": " + str(msg.content)
    toWrite = userMsg + '\n'
    print(userMsg)
    with open("logs.txt", "a", encoding='utf-8') as myFile:
        myFile.write(toWrite)


# Check the value assigned to trigger word and handle appropriately
async def send_message(msg, key):
    # If string starts with ./ assume directory for file
    if calls[key][:2] == './':
        with open(calls[key], 'rb') as fileDir:
            await msg.channel.send(file=discord.File(fileDir))
    # Otherwise treat as string
    else:
        await msg.channel.send(calls[key])


# Trigger function when message is sent to the server
@client.event
async def on_message(message):
    # Log message
    log(message)

    # Stop bot from reading own messages
    if message.author == client.user:
        return None

    # Set lower and remove whitespace
    lowerMsg = message.content.lower()
    condensedMsg = lowerMsg.replace(" ", "")

    # Check message against dictionary of trigger words
    for key in calls:
        # If trigger word is longer than 4 char find with trim
        if len(key) >= 4:
            if condensedMsg.find(key) != -1:
                await send_message(message, key)
        # If trigger is less than 4 words find whole
        elif len(key) < 4:
            if re.search(r"\b" + re.escape(key) + r"\b", lowerMsg):
                await send_message(message, key)


print('Bot is up')
client.run(token)
