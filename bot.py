import discord
from discord.ext import commands

try:
    with open("token.prv", "r") as f:
        TOKEN = f.readline()
except FileNotFoundError:
    print('File with bot token not found')
    raise

client = commands.Bot(command_prefix = '!alma ')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

#answers with the ms latency
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round (client.latency * 1000)}ms ')

#answers with the ms latency
@client.command()
async def hello(ctx):
    await ctx.send("Hello, {}. Now get back to work.".format(ctx.message.author.mention))

@client.command()
async def image(ctx):
    await ctx.channel.send(file=discord.File('ironic_palpatine.png'))
    await ctx.send("Hello, {}. Here is your image.".format(ctx.message.author.mention))


client.run(TOKEN)