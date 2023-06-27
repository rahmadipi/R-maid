import discord
import os
import requests
import json
import random
#import replit
from replit import db
from keep_alive import keep_alive
from discord.ext import commands

prefix = "r-"
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(case_insensitive=True,
                   command_prefix=prefix,
                   intents=intents)

db.clear()


@bot.event
async def on_ready():
  # activity = discord.Streaming(name="My Stream",
  #                              url="https://youtu.be/sLzEbo8nQ8Q")
  # activity = discord.Activity(type=discord.ActivityType.listening,
  #                             name="R-unknown's ASMR")
  # activity = discord.Activity(type=discord.ActivityType.watching,
  #                             name="ur mom")
  activity = discord.Game("with R-unknown")
  await bot.change_presence(status=discord.Status.dnd, activity=activity)
  print('logged in as {0.user}'.format(bot))


#init help
def helpEmbed():
  embed = discord.Embed(
    title="House Navigation",
    #url="https://realdrewdata.medium.com/",
    description="Rules to request my services",
    color=discord.Color.dark_red())

  embed.add_field(name="Command rules",
                  value="My prefix is `" + prefix + "`,\n" +
                  "It's case insensitive so `" + prefix + "` and `" +
                  prefix.upper() + "` would work !\n" +
                  "btw don't call my master name so casually :rage:",
                  inline=False)

  embed.add_field(name="Command list", value="", inline=False)

  embed.add_field(name="",
                  value="`" + prefix + "help` (`h`)\n" +
                  "get to know me better :heart:",
                  inline=False)

  embed.add_field(name="",
                  value="`" + prefix + "weather` (`w`) + `{city}`\n" +
                  "get weather details of the specific city",
                  inline=False)

  embed.add_field(name="",
                  value="`" + prefix + "quote` (`q`)\n" +
                  "get random quote for ur motivation",
                  inline=False)

  embed.add_field(name="", value="", inline=False)
  embed.add_field(name="Slash Command list", value="", inline=False)

  embed.add_field(name="",
                  value="`/help`\n" + "get to know me better :heart:",
                  inline=False)

  embed.add_field(name="",
                  value="`/hi` + `[name]`\n" + "greet me :wave:",
                  inline=False)

  embed.add_field(name="",
                  value="`/avatar` + `[mention a user]`\n" +
                  "show the user avatar",
                  inline=False)

  return embed


#end of init help


#init avatar
def avatarEmbed(user):
  embed = discord.Embed(title=user.name,
                        url=user.avatar,
                        description=f"{user.name}'s avatar",
                        color=discord.Color.dark_red())

  embed.set_image(url=user.avatar)

  return embed


#end of init avatar

#init db
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

#init encouragement
sad_words = ["sad", "depressed", "cry", "kms"]
starter_encouragements = [
  "Cheer up", "It's okay dude, I'm here", "u okay bro ?"
]

if "responding" not in db.keys():
  db["responding"] = False


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


#slash commands
@bot.slash_command(description="Greet your lovely maid.")
async def hi(ctx, name: str = None):
  name = name or ctx.author.name
  await ctx.respond(f"Henlo {name}!")


@bot.slash_command(description="Ask your maid how to command her.")
async def help(ctx):
  embed = helpEmbed()
  await ctx.respond(embed=embed)


@bot.slash_command(description="3.. 2.. 1.. Cheeze !")
async def avatar(ctx, user: discord.Member = None):
  user = user or ctx.author
  embed = avatarEmbed(user)
  await ctx.respond(embed=embed)


# async def avatar(ctx):
#   user = ctx.author
#   embed = avatarEmbed(user)
#   await ctx.respond(embed=embed)

#end of slash commands


@bot.event
async def on_message(message):
  if message.author == bot.user: return

  msg = message.content.lower()

  #help methods
  if (msg.startswith(f"{prefix}h") or msg.startswith(f"{prefix}help")):
    embed = helpEmbed()
    await message.channel.send(embed=embed)
  #end of help methods

  #avatar methods
  # coming soon
  #end of avatar methods

  #greet methods
  if msg.startswith(f"{prefix}henlo"):
    await message.channel.send('Hai! goshujin-sama!')
  #end of greet methods

  #praise methods
  if (msg.rfind("R-unknown") != -1 or msg.rfind("r-unknown") != -1
      or msg.rfind("runknown") != -1 or msg.rfind("268063580170092544") != -1):
    await message.channel.send(random.choice(db["praise"]))
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
      temperature = get_weather("" + city)
      await message.channel.send(temperature)
    except:
      try:
        city = msg.split(f"{prefix}weather ", 1)[1]
        temperature = get_weather("" + city)
        await message.channel.send(temperature)
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

  #dm methods
  # if msg.startswith(f"{prefix}dm"):
  #   dm = msg.split(f"{prefix}dm ", 1)[1]
  #   user = bot.get_user(268063580170092544)
  #   await user.send(dm)
  #end of dm methods


keep_alive()
try:
  bot.run(os.getenv('TOKEN'))
except discord.HTTPException as e:
  if e.status == 429:
    print(
      "The Discord servers denied the connection for making too many requests")
  else:
    raise e
