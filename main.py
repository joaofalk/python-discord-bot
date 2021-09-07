import discord
import os
import random
from discord import member
from discord.ext.commands.core import command
from discord.flags import Intents
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN']
GUILD_ID = os.environ['DISCORD_SERVER_ID']

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='#', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@bot.command(name='Ping', help='Responds Pong!')
async def ping_pong(ctx):
    response_text = 'Pong!'
    response = response_text
    await ctx.send(response)


@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    sum_of_rolls = 0
    for number in dice:
        sum_of_rolls += int(number)

    response_text = f"{', '.join(dice)}. The sum of your roll is: {sum_of_rolls}"

    await ctx.send(response_text)


@bot.command(name='create-channel', help='creates channel')
@commands.has_role('Dono do Server')
async def create_channel(ctx, channel_name='Basic Bitch'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)
