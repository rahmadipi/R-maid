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
color = discord.Color.dark_red()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(case_insensitive=True,
                   command_prefix=prefix,
                   intents=intents)
wrongFormat = "fix ur command format please !"

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
  commandRules = f"\
  My prefix is `{prefix}`\
  \nIt's case insensitive so `{prefix}` and `{prefix.upper()}` would work !\
  \nbtw don't call my master name so casually :rage:\n\n"

  commandList = f"\
  :dizzy: **`{prefix}help` (`h`)**\
  \nget to know me better :heart:\
  \n:dizzy: **`{prefix}weather` (`w`) + `{{city}}`**\
  \nget weather details of the specific city\
  \n:dizzy: **`{prefix}quote` (`q`)**\
  \nget random quote for ur motivation\
  \n:dizzy: **`{prefix}gif` (`g`) + `{{keywords}}`**\
  \nlemme find the gif using your keywords\n\n"

  slashCommand = "\
  :dizzy: **`/help`**\
  \nget to know me better :heart:\
  \n:dizzy: **`/hi`**\
  \ngreet me :wave:\
  \n:dizzy: **`/avatar` + `[mention a user]`**\
  \nshow the user avatar\n\n"

  embed = discord.Embed(title="House Navigation",
                        description="Rules to request my services",
                        color=color)

  embed.add_field(name="Command rules", value=commandRules, inline=False)

  embed.add_field(name="Command list", value=commandList, inline=False)

  embed.add_field(name="Slash Command list", value=slashCommand, inline=False)

  return embed


#end of init help


#init avatar
def avatarEmbed(user):
  embed = discord.Embed(title=user.name,
                        url=user.avatar,
                        description=f"{user.name}'s avatar",
                        color=color)

  embed.set_image(url=user.avatar)

  return embed


#end of init avatar

#init clingy
if "clingy" not in db.keys():
  db["clingy"] = True

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
#end of init clingy

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
  quote = f"\
  >>> \"_{json_data[0]['q']}_\"\
  \n\n-**{json_data[0]['a']}**"

  return (quote)


#end of init quote


#init weather
def initWeather(data):
  temperature = f"\
  **Weather**\
  \n{data['weather'][0]['description'].capitalize()}\
  \n**Temperature**\
  \n{data['main']['temp']} ℃\
  ({data['main']['temp_min']} ℃ - {data['main']['temp_max']} ℃)\
  \n**Humidity**\
  \n{data['main']['humidity']} %\
  \n**Atmospheric pressure**\
  \n{data['main']['pressure']} hPa\
  \n**Wind speed**\
  \n{data['wind']['speed']} m/s\
  \n**Cloudiness**\
  \n{data['clouds']['all']} %\n\n"

  embed = discord.Embed(title=data['name'] + " weather", color=color)
  embed.add_field(name="", value=temperature, inline=False)
  embed.set_thumbnail(
    url=f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
  )
  return embed


def get_weather(city):
  data = []
  response = requests.get(
    "https://api.openweathermap.org/data/2.5/weather?q=" + city +
    "&units=metric&appid=" + os.getenv('WEATHER_KEY') + "")
  json_data = json.loads(response.text)
  if str(json_data['cod']) != "404":
    data = json_data
    res = True
  else:
    res = False
  respon = [res, data]
  return (respon)


#end of init weather


#init gif
def gifEmbed(search):
  embed = None
  dataSize = 10
  response = requests.get(
    "https://api.giphy.com/v1/gifs/search?api_key=" + os.getenv('GIPHY_KEY') +
    "&q=" + search + "&limit=" + str(dataSize) +
    "&offset=0&rating=g&lang=en&bundle=messaging_non_clips")
  json_data = json.loads(response.text)
  if str(json_data['meta']['status']) == "200":
    rand = random.randint(0, (dataSize - 1))
    url = json_data['data'][rand]['url']
    gif = json_data['data'][rand]['images']['fixed_height']['url']
    embed = discord.Embed(title="", url=url, description="", color=color)
    embed.set_image(url=gif)
    res = True
  else:
    res = False
  respon = [res, embed]
  return respon


#end of init gif


#slash commands
@bot.slash_command(description="Greet your lovely maid.")
async def hi(ctx):
  name = ctx.author.name
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
async def on_member_join(member):
  # R-maid HQ server
  guildId: int = 1120003050002710550
  roleId: int = 1124148992272498698
  # R-lab server
  # guildId: int = 898743465465225256
  # roleId: int = 1124164614763053197
  # roleName = "tester"
  if member.guild.id == guildId:
    try:
      #role = discord.utils.get(member.guild.roles, name=roleName)
      role = discord.utils.get(member.guild.roles, id=roleId)
      await member.add_roles(role)
    except:
      pass


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

  #cling methods
  if msg.startswith(f"{prefix}clingy"):
    clingyOff = "aight, i will keep my dignity as your maid :pensive:"
    clingyOn = "YES MASTER, i will always on ur side :heart:"
    clingyFail = "what do you want ?"
    try:
      value = msg.split(f"{prefix}clingy ", 1)[1]
      if value.lower() == "on":
        db["clingy"] = True
        await message.channel.send(clingyOn)
      elif value.lower() == "off":
        db["clingy"] = False
        await message.channel.send(clingyOff)
      else:
        await message.channel.send(clingyFail)
    except:
      if db["clingy"]:
        db["clingy"] = False
        await message.channel.send(clingyOff)
      else:
        db["clingy"] = True
        await message.channel.send(clingyOn)

  if db["clingy"]:
    if (msg.rfind("R-unknown") != -1 or msg.rfind("r-unknown") != -1
        or msg.rfind("runknown") != -1
        or msg.rfind("268063580170092544") != -1):
      await message.channel.send(random.choice(db["praise"]))
  #end of clingy methods

  #quote methods
  if (msg.startswith(f"{prefix}q") or msg.startswith(f"{prefix}quote")):
    quote = get_quote()
    await message.channel.send(quote)
  #end of quote methods

  #gif methods
  if (msg.startswith(f"{prefix}g") or msg.startswith(f"{prefix}gif")):
    gifFail = "umm something went wrong"
    try:
      search = msg.split(f"{prefix}g ", 1)[1]
      respon = gifEmbed("" + search)
      if respon[0]:
        embed = respon[1]
        await message.channel.send(embed=embed)
      else:
        await message.channel.send(gifFail)
    except:
      try:
        search = msg.split(f"{prefix}gif ", 1)[1]
        respon = gifEmbed("" + search)
        if respon[0]:
          embed = respon[1]
          await message.channel.send(embed=embed)
        else:
          await message.channel.send(gifFail)
      except:
        await message.channel.send(wrongFormat)
  #end of gif methods

  #weather methods
  if (msg.startswith(f"{prefix}w") or msg.startswith(f"{prefix}weather")):
    weatherFail = "u sure that city exist ?"
    try:
      city = msg.split(f"{prefix}w ", 1)[1]
      respon = get_weather("" + city)
      if respon[0]:
        embed = initWeather(respon[1])
        await message.channel.send(embed=embed)
      else:
        await message.channel.send(weatherFail)
    except:
      try:
        city = msg.split(f"{prefix}weather ", 1)[1]
        respon = get_weather("" + city)
        if respon[0]:
          embed = initWeather(respon[1])
          await message.channel.send(embed=embed)
        else:
          await message.channel.send(weatherFail)
      except:
        await message.channel.send(wrongFormat)
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
