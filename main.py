import discord
from discord.ext import commands

# Your user ID
OWNER_ID = 1317632570468335698

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Track messages to be able to resend
tracked_messages = {}

@bot.event
async def on_message(message):
    # Ignore messages from bots (except this bot for tracking)
    if message.author.bot and message.author != bot.user:
        return

    # Track messages sent by the owner or the bot
    if message.author.id == OWNER_ID or message.author == bot.user:
        tracked_messages[message.id] = {
            "content": message.content,
            "channel": message.channel,
            "author": message.author
        }

    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    # If it's one of our tracked messages
    if message.id in tracked_messages:
        msg_info = tracked_messages[message.id]
        channel = msg_info["channel"]
        author = msg_info["author"]
        
        # Only resend if someone else deleted it
        if message.author != bot.user and message.author.id != OWNER_ID:
            await channel.send(f"(Restored) {author.mention}: {msg_info['content']}")

# Optional: Command to clear bot messages, only for you
@bot.command()
async def deletebot(ctx, message_id: int):
    if ctx.author.id != OWNER_ID:
        return await ctx.send("You can't do that!")
    try:
        msg = await ctx.channel.fetch_message(message_id)
        if msg.author == bot.user:
            await msg.delete()
            await ctx.send("Deleted!")
        else:
            await ctx.send("This is not a bot message.")
    except:
        await ctx.send("Message not found.")

# Run your bot
bot.run("YOUR_BOT_TOKEN")
