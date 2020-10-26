import discord
from discord.ext import commands
import logging
import glob
import os
import sys
import random
import traceback
from logging.handlers import RotatingFileHandler
from saygeek.saygeek import SayGeek
import config as cfg

# Setup logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(filename=cfg.LOG_FILENAME, maxBytes=50000000, backupCount=5, encoding='utf-8')
handler.setFormatter(logging.Formatter(cfg.LOG_FORMAT_BASE))
logger.addHandler(handler)

# Get token for bot
try:
    with open("token.prv", "r") as f:
        TOKEN = f.readline()
except FileNotFoundError:
    logger.info('File with bot token not found')
    raise

client = commands.Bot(command_prefix = cfg.COMMAND_PREFIX)

@client.event
async def on_command_error(ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandOnCooldown, )

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CommandNotFound):
            await ctx.message.channel.send('You must give a valid command, my friend. Try !alma help')
            logger.info('Wrong command {} by {}'.format(ctx.command.qualified_name, ctx.message.author.display_name))

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')
            logger.info(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                await ctx.send('I could not find that member. Please try again.')

        else:
            # All other Errors not returned come here. And we can just logthe default TraceBack.
            logger.info('Ignoring exception in command {} by user {}:'.format(ctx.command, ctx.message.author.display_name))
            logger.info(''.join(traceback.format_exception(type(error), error, error.__traceback__)))

@client.event
async def on_ready():
    '''Create a log entry when client is initialized'''
    logger.info('We have logged in as {0.user}'.format(client))

@client.command(
    brief="Show an ALMA meme. Pero con respeto ¯\_(ツ)_/¯",
    help="Show an ALMA meme. Pero con respeto ¯\_(ツ)_/¯\n" + \
         "Defaults to give you a random meme. Add 'latest' for...well, you can guess what."
)
async def meme(ctx, option: str = None):
    '''Send an ALMA meme'''

    meme_list = glob.glob(os.path.join(cfg.MEMES_PATH_TO_FOLDER, '*.jpg')) + \
        glob.glob(os.path.join(cfg.MEMES_PATH_TO_FOLDER, '*.png'))

    if not meme_list:
        await ctx.message.channel.send('No meme was found. This is a real emergency. Contact a meme specialist.')
        logger.info('{}/#{} - Memes not found in folder {}'.format(ctx.message.guild.name, ctx.message.channel.name, cfg.MEMES_PATH_TO_FOLDER))
    else:
        if option is None or option == "random":
            random.seed(os.getrandom(10))
            chosen_meme = random.choice(meme_list)
        elif option == 'latest':
            meme_list.sort(key=os.path.getmtime)
            chosen_meme = meme_list[-1]
            logger.info('{}/#{} - Latest meme requested by {}'.format(
                ctx.message.guild.name, ctx.message.channel.name, ctx.message.author.display_name)
            )
        else:
            random.seed(os.getrandom(10))
            chosen_meme = random.choice(meme_list)
            await ctx.send(f'{option} is not a valid option. Just giving you a random meme so you don\'t leave empty handed.')
            logger.info(f'Invalid {option} for command meme')

        await ctx.channel.send(file=discord.File(chosen_meme))
        logger.info('{}/#{} - Sending meme {} requested by {}'.format(
            ctx.message.guild.name, ctx.message.channel.name, chosen_meme, ctx.message.author.display_name)
        )

@client.command(
    brief="Show a historical geek phrase from ALMA",
    help="I'll give you a notable phrase or similar said by a member of ALMA staff.\n" + \
          "For example, for Control Room madness, try !alma saygeek AOG \n" + \
          "Try !alma saygeek keys for all available categories."
)
async def saygeek(ctx, phrase_key: str = None):
    '''Send a phrase from a number of available categories'''

    sg = SayGeek('saygeek/saygeek.db')
    msg_help = 'Accepted keys are:\n{}\n\nExample: !alma saygeek ALMA'.format('\n'.join(sorted(sg.keys)))

    if phrase_key in ['help', 'HELP', 'Help', 'keys', 'KEYS']:
        await ctx.send(msg_help)
    elif phrase_key is None:
        await ctx.send(msg_help)
    else:
        if phrase_key.upper() in sg.keys:
            data = sg.random_phrase(phrase_key.upper())
            header = '[{}]:\n'.format(data['prefix']) if data['prefix'] else ''
            await ctx.send('{}{}'.format(header, data['phrase']))
            logger.info('{}/#{} - [{}] Phrase requested by {} ({}...{})'.format(
                ctx.message.guild.name,
                ctx.message.channel.name,
                phrase_key.upper(),
                ctx.message.author.display_name,
                data['phrase'][:10], data['phrase'][-10:])
            )
        else:
            await ctx.send(msg_help)

client.run(TOKEN)
