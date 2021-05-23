# self info 
from data import downloader
from data.bot_token import bot_token 
# libraries
import discord 
from discord.ext import commands

prefix = "popbot "
bot = commands.Bot(command_prefix=prefix)

# login message 
@bot.event
async def on_ready():
    # prints in terminal that bot is online
    print('We have logged in as {0.user}'.format(bot))

# message reader 
@bot.event
async def on_message(message):
    # ignore self 
    if message.author == bot.user:
        return

    # does command if there is prefix leading message
    await bot.process_commands(message)

# bot commands

# beginner example command
@bot.command()
async def foo(ctx, *args):
    await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))

@bot.command()
async def addEmote(ctx, *args):
    # to do
    # verify name isn't taken
    
    # verify attachment is present
    if 0 < len(ctx.message.attachments) == len(args):
        # for index in range (len(args)):
            # downloader.processDiscordAttachment(attachment, emote_name)
        await ctx.send(ctx.message.attachments[0])
    else:
        await ctx.send("Missing Pictures to Use As Emotes")
    print(ctx.message.attachments)
    

if __name__ == "__main__":
    bot.run(bot_token)