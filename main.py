# self info 
from data import emote_manager
from data.bot_token import bot_token 
# libraries
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
        for index in range (len(args)):
            addcode = emote_manager.processDiscordAttachment(ctx.message.attachments[index], args[index])
            if addcode == 1:
                await ctx.send(f'{args[index]} is already taken as an emote name')
            elif addcode == 2:
                await ctx.send('That is not a supported filetype')
            else:
                await ctx.send('Emote has been successfully stored')
    else:
        await ctx.send("Missing Pictures to Use As Emotes")
    print(ctx.message.attachments)
    

if __name__ == "__main__":
    bot.run(bot_token)