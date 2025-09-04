import discord
from discord.ext import commands

# Your Discord user ID
YOUR_USER_ID = 1317632570468335698

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Store a mapping of bot reposts to the original content
repost_memory = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message_delete(message):
    # If the deleted message is yours, repost it
    if message.author.id == YOUR_USER_ID:
        content = message.content
        if content:
            repost = await message.channel.send(f"(Reposted) {message.author.name} said: {content}")
            repost_memory[repost.id] = content

    # If the deleted message is a bot repost
    elif message.author == bot.user:
        if message.id in repost_memory:
            # If the deleter is NOT you, repost again
            # Discord.py doesn't give deleter info by default, so this works if only you can manually delete
            # Otherwise, the bot reposts regardless
            repost = await message.channel.send(f"(Reposted again) {YOUR_USER_ID} said: {repost_memory[message.id]}")
            repost_memory[repost.id] = repost_memory[message.id]

bot.run("YOUR_BOT_TOKEN")
