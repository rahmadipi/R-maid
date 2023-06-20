#from discord.ext import commands
import discord
import os
import requests
import json
import random
#import replit
from replit import db
from keep_alive import keep_alive
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(case_insensitive=True, intents=intents)

sad_words = ["sad", "depressed", "angery"]

starter_encouragements = ["Cheer up", "Hang in there"]

db.clear()

if "responding" not in db.keys():
  db["responding"] = True

default_prefix = "r-"

def get_all_guild_id():
  db["server_ids"] = []
  db["prefixs"] = [{}]
  for i in client.guilds:
    if i.guild.id not in db["server_ids"]:
      db["server_ids"] = db["server_ids"].append(i.guild.id)
    if i.guild.id not in db["prefixs"]:
      db["prefixs"].update = ({str(i.guild.id): default_prefix})


get_all_guild_id()
  
def update_encouragement(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]


def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)


def get_weather(city):
  response = requests.get(
    "https://api.openweathermap.org/data/2.5/weather?q=" + city +
    "&units=metric&appid=" + os.getenv('WEATHER_KEY') + "")
  json_data = json.loads(response.text)
  if str(json_data['cod']) != "404":
    pesan = "Temperature = " + str(json_data['main']['temp']) + "°C"
  else:
    pesan = "Kota tidak ditemukan!"
  return (pesan)


@client.event
async def on_ready():
  print('logged in as {0.user}'.format(client))

@commands.command()
async def embed(ctx):
  embed = discord.Embed(
    title="Sample Embed",
    url="https://realdrewdata.medium.com/",
    description=
    "This is an embed that will show how to build an embed and the different components",
    color=discord.Color.blue())
  await ctx.send(embed=embed)


@client.event
async def on_message(message):
  prefix = default_prefix
  if message.author == client.user: return

  msg = message.content

  if msg.startswith(f"{prefix}henlo"):
    await message.channel.send('Hai! goshujin-sama!')

  if (msg.rfind("R-unknown") != -1 or msg.rfind("r-unknown") != -1
      or msg.rfind("runknown") != -1):
    await message.channel.send("R-unknown-sama ! That's my master ! :heart:")

  if msg.startswith(f"{prefix}dm"):
    dm = msg.split("$dm ", 1)[1]
    user = client.get_user(268063580170092544)
    await user.send(dm)

  #if msg.startswith(f"{prefix}help"):

  if msg.startswith(f"{prefix}quote"):
    quote = get_quote()
    await message.channel.send(quote)

  if msg.startswith(f"{prefix}w"):
    try:
      city = msg.split(f"{prefix}w ", 1)[1]
      weather = get_weather("" + city)
      await message.channel.send(weather)
    except:
      await message.channel.send("format perintah salah woy !")

  if msg.startswith(f"{prefix}new"):
    encouraging_message = msg.split("$new ", 1)[1]
    update_encouragement(encouraging_message)
    await message.channel.send("Added!")

  if msg.startswith(f"{prefix}del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split(f"{prefix}del", 1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith(f"{prefix}list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith(f"{prefix}responding"):
    value = msg.split(f"{prefix}responding ", 1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")


@client.slash_command(guild_ids=db["server_ids"],
                      name="hi",
                      description="greet the bot")
async def hi(ctx: discord.ApplicationContext):
  await ctx.respond("Henlo !")


keep_alive()
client.run(os.getenv('TOKEN'))
