import discord
import os
import requests
import json
import random
#import replit
from replit import db
from keep_alive import keep_alive
from discord.ext import commands

default_prefix = "r-"
db["server_ids"] = [1120003050002710550]
guild_ids = db["server_ids"]
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(case_insensitive=True,
                   command_prefix=default_prefix,
                   intents=intents)

db.clear()


@bot.event
async def on_ready():
  print('logged in as {0.user}'.format(bot))


#init help
def helpEmbed():
  embed = discord.Embed(
    title="House Navigation",
    #url="https://realdrewdata.medium.com/",
    description="Rules to request my services",
    color=discord.Color.dark_red())

  embed.add_field(
    name="Command rules",
    value="Command me by send `r-`+`{commands}`+`[variables]`\n" +
    "`variables` are optional\n" +
    "for `commands` you can pick from command list below",
    inline=False)

  embed.add_field(name="Command", value="", inline=True)
  embed.add_field(name="Service", value="", inline=True)
  #list below
  embed.add_field(name="", value="`help` (`h`)", inline=False)
  embed.add_field(name="", value="get to know me better", inline=False)
  embed.add_field(name="",
                  value="`temperature` (`t`) `+` `{city name}`",
                  inline=False)
  embed.add_field(name="", value="get the ", inline=True)

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

# for guild in bot.guilds:
#   if guild.id not in guild_ids:
#     guild_ids = guild_ids.append(guild.id)
#     print(guild.id)
#   if guild.id not in db["prefixes"]:
#     db["prefixes"] = guild_ids.append([guild.id, default_prefix])
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


#init temperature
def get_temperature(city):
  response = requests.get(
    "https://api.openweathermap.org/data/2.5/weather?q=" + city +
    "&units=metric&appid=" + os.getenv('WEATHER_KEY') + "")
  json_data = json.loads(response.text)
  if str(json_data['cod']) != "404":
    pesan = "Temperature = " + str(json_data['main']['temp']) + "°C"
  else:
    pesan = "Kota tidak ditemukan!"
  return (pesan)


#end of init temperature


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
async def avatar(ctx):
  user = ctx.author
  embed = avatarEmbed(user)
  await ctx.respond(embed=embed)


# async def avatar(ctx, user=discord.Member):
#   user = ctx.get_user(user.id) or ctx.author
#   embed = avatarEmbed(user)
#   await ctx.respond(embed=embed)

#end of slash commands


# @commands.command()
# async def embed(interaction):
#   embed = discord.Embed(
#     title="Sample Embed",
#     url="https://realdrewdata.medium.com/",
#     description=
#     "This is an embed that will show how to build an embed and the different components",
#     color=discord.Color.blue())
#   await interaction.send(embed=embed)
@bot.command()
async def ping(ctx: discord.ApplicationContext):
  await ctx.send("pong")


@bot.event
async def on_message(message):
  prefix = default_prefix
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
      or msg.rfind("runknown") != -1):
    await message.channel.send(random.choice(db["praise"]))
  #end of praise methods

  #quote methods
  if (msg.startswith(f"{prefix}q") or msg.startswith(f"{prefix}quote")):
    quote = get_quote()
    await message.channel.send(quote)
  #end of quote methods

  #temperature methods
  if (msg.startswith(f"{prefix}t") or msg.startswith(f"{prefix}temperature")):
    try:
      city = msg.split(f"{prefix}t ", 1)[1]
      temperature = get_temperature("" + city)
      await message.channel.send(temperature)
    except:
      try:
        city = msg.split(f"{prefix}temperature ", 1)[1]
        temperature = get_temperature("" + city)
        await message.channel.send(temperature)
      except:
        await message.channel.send("format perintah salah woy !")
  #end of temperature methods

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
