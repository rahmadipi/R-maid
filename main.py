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
bot = commands.Bot(case_insensitive=True, intents=intents)

db.clear()

#init db
default_prefix = "r-"
db["server_ids"] = [1120003050002710550]
db['praise'] = [
  "R-unknown-sama ! That's my master ! :heart:",
  "did anyone call my Goshujin-sama ?",
  "hehe R-unknown is my master ! my beloved goshujin-sama :heart: :heart:",
  "ikr, R-unknown-sama is the best of the best hehe :flushed:",
  "don't steal my R-unknown-sama or i might bite u, grrrrr.. :rage:",
  "R-unknown-sama please marry me, kyaaaa >_<",
  "don't call my master's name so casually !! ask my permission first ! :angry:",
  "hey, don't get too close with my master :pensive:",
]
"""
for guild in bot.guilds:
  if guild.id not in db["server_ids"]:
    db["server_ids"] = db["server_ids"].append(guild.id)
    print(guild.id)
  if guild.id not in db["prefixes"]:
    db["prefixes"] = db["server_ids"].append([guild.id, default_prefix])
"""
#end of init db

#init encouragement
sad_words = ["sad", "depressed", "cry", "kms"]
starter_encouragements = [
  "Cheer up", "It's okay dude, I'm here", "u okay bro ?"
]

if "responding" not in db.keys():
  db["responding"] = True


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


#end of init encouragement


#init quote
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return (quote)


#end of init quote


#init weather
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


#end of init weather


@bot.event
async def on_ready():
  print('logged in as {0.user}'.format(bot))


#slash commands
@bot.slash_command(guild_ids=db["server_ids"],
                      name="hi",
                      description="greet the bot")
async def hi(ctx: discord.ApplicationContext):
  await ctx.respond("Henlo !")


#end of slash commands
"""
@commands.command()
async def embed(ctx):
  embed = discord.Embed(
    title="Sample Embed",
    url="https://realdrewdata.medium.com/",
    description=
    "This is an embed that will show how to build an embed and the different components",
    color=discord.Color.blue())
  await ctx.send(embed=embed)
"""


@bot.event
async def on_message(message):
  prefix = default_prefix
  if message.author == bot.user: return

  msg = message.content

  #greet methods
  if msg.startswith(f"{prefix}henlo"):
    await message.channel.send('Hai! goshujin-sama!')
  #end of greet methods

  #praise methods
  if (msg.rfind("R-unknown") != -1 or msg.rfind("r-unknown") != -1
      or msg.rfind("runknown") != -1):
    await message.channel.send(db["praise"][random.randint(
      0, (len(db["praise"]) - 1))])
  #end of praise methods

  #quote methods
  if (msg.startswith(f"{prefix}q") or msg.startswith(f"{prefix}quote")):
    quote = get_quote()
    await message.channel.send(quote)
  #end of quote methods

  #weather methods
  if (msg.startswith(f"{prefix}w") or msg.startswith(f"{prefix}weather")):
    try:
      city = msg.split(f"{prefix}w ", 1)[1]
      weather = get_weather("" + city)
      await message.channel.send(weather)
    except:
      try:
        city = msg.split(f"{prefix}weather ", 1)[1]
        weather = get_weather("" + city)
        await message.channel.send(weather)
      except:
        await message.channel.send("format perintah salah woy !")
  #end of weather methods

  #encouragement methods
  if msg.startswith(f"{prefix}new"):
    encouraging_message = msg.split(f"{prefix}new ", 1)[1]
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
  #end of encouragement methods
  """
  #dm methods
  if msg.startswith(f"{prefix}dm"):
    dm = msg.split(f"{prefix}dm ", 1)[1]
    user = bot.get_user(268063580170092544)
    await user.send(dm)
  #end of dm methods

  #help methods
  if msg.startswith(f"{prefix}help"):
  #end of help methods
  """


keep_alive()
bot.run(os.getenv('TOKEN'))
