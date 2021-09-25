import discord
import os
import random
from discord import member
from discord.ext.commands.core import command
from discord.flags import Intents
from dotenv import load_dotenv
from discord.ext import commands
from aerisweather.aerisweather import AerisWeather
from aerisweather.requests.RequestLocation import RequestLocation

load_dotenv()

TOKEN = os.environ['DISCORD_TOKEN']
aeris = AerisWeather(client_id=os.environ['CLIENT_ID'],
                     client_secret=os.environ['CLIENT_SECRET'], app_id=os.environ['APP_ID'])
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


@bot.command(name='weather', help='Gets weather info of a particular city')
async def get_weather(ctx, city_name: str, state: str):
    location = RequestLocation(city=city_name, state=state)
    observation_list = aeris.observations(location=location)

    for observation in observation_list:
        place = observation.place
        ob = observation.ob
        tempF = ob.tempF
        weather = ob.weather

        response_text = f"""
        The current weather for {place.name.capitalize()}, {place.state.upper()} is: 
Conditions are current {weather} with a temp of {tempF} Fº
"""

        await ctx.send(response_text)


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
