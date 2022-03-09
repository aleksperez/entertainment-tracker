import discord
from discord.ext import commands
import psycopg2
import random
import os
from dotenv import load_dotenv
from tmdb import *

load_dotenv()
TOKEN = os.getenv('TOKEN')
USER= os.getenv("user")
PASS= os.getenv("password")
DB= os.getenv("database")
DB_URI= os.getenv("DB_URI")
HOST = os.getenv("HOST")
RED = 15158332
BLUE = 3447003
#have python choose random number between 1 - (total index num of database) and then retrieve value for that random index

movies='''CREATE TABLE MOVIES(
    ID SERIAL,
    MOVIE VARCHAR(200)
)'''

shows='''CREATE TABLE SHOWS(
    ID SERIAL,
    SHOW VARCHAR(200)
)'''

games='''CREATE TABLE GAMES(
    ID SERIAL,
    GAME VARCHAR(200)
)'''

connection = psycopg2.connect(
    user = USER,
    password = PASS,
    host = HOST,
    port = "5432",
    database = DB
)
cursor = connection.cursor()
#MOVIES DATA
def addMovie(movieTitle):
    query= '''INSERT INTO MOVIES(MOVIE) VALUES ('%s')''' % movieTitle
    cursor.execute(query);
    connection.commit();

def deleteMovie(movie):
    query='''DELETE FROM MOVIES WHERE MOVIE = '%s' ''' % movie
    cursor.execute(query)
    connection.commit();

def getMovie():
    num = random.randint(0,getSize('MOVIES')-1)
    data=getTable('MOVIES')
    return data[num][1]

#SHOWS DATA
def addShow(showTitle):
    query= '''INSERT INTO SHOWS(SHOW) VALUES ('%s')''' % showTitle
    cursor.execute(query);
    connection.commit();

def deleteShow(show):
    query='''DELETE FROM SHOWS WHERE SHOW = '%s' ''' % show
    cursor.execute(query)
    connection.commit();

def getShow():
    num = random.randint(0,getSize('SHOWS')-1)
    data=getTable('SHOWS')
    return data[num][1]

#GAMES DATA
def addGame(game):
    query= '''INSERT INTO GAMES(GAME) VALUES ('%s')''' % game
    cursor.execute(query);
    connection.commit();

def deleteGame(game):
    query='''DELETE FROM GAMES WHERE GAME = '%s' ''' % game
    cursor.execute(query)
    connection.commit();

def getGame():
    num = random.randint(0,getSize('GAMES')-1)
    data=getTable('GAMES')
    return data[num][1]

#generic table information
def getSize(table):
    query='''SELECT COUNT(*) from %s ''' % table
    cursor.execute(query)
    result = cursor.fetchall();
    return result[0][0];

def getTable(table):
    cursor.execute('''SELECT * from %s'''% table)
    result = cursor.fetchall();
    return result;

def formatList(table, tableList):
    prettyList = f"**{table.upper()}** LIST:\n\n"
    for item in tableList:
        prettyList+= f"- {item[1].capitalize()}\n"
    return prettyList


def getUserId(ctx,person):
    for i in range(len(ctx.guild.members)):
        if person == ctx.guild.members[i].nick:
            userId= ctx.guild.members[i].id
            return userId

commandString= '''-movie\n-show\n-game\n\n-addmovie movietitle\n-delmovie movietitle\n\n-addshow showtitle\n-delshow showtitle\n\n-addgame gametitle\n-delgame gametitle\n\n-movielist\n-showlist\n-gamelist'''


intents= discord.Intents
client = commands.Bot(command_prefix='-', intents=intents.all())

#EVENTS
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#COMMANDS
@client.command()
async def ping(ctx,arg):
    userid = getUserId(ctx,arg)
    await ctx.author.send(userid) 

@client.command()
async def commands(ctx):
    await ctx.author.send(commandString)

@client.command()
async def nickname(ctx,arg):
    try:
        await ctx.author.edit(nick=arg)
        await ctx.send(f"updated nickname to {arg}")
    except:
        await ctx.send("command didn't work... try again! Type **-commands** for formatting rules")

@client.command()
async def clear(ctx,amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()
async def movie(ctx):
    try:
        movieName = getMovie().capitalize()
        json = get_json('movie', movieName)['results'][0]
        poster= get_poster(json)
        providers=get_providers('movie',get_id(json))
        description = get_overview(json)
        prettyproviders=""
        for i in providers:
            if len(providers) > 1:
                prettyproviders+=i+',    '
            prettyproviders+= i
        embed = discord.Embed(title=movieName, description=description, color=RED)
        embed.set_image(url = poster)
        if providers:
            embed.add_field(name="Currently Streaming On:", value=prettyproviders)
        else:
            embed.add_field(name="Not streaming anywhere :(", value="\u200b")
        await ctx.send(embed=embed)
    except:
        await ctx.send("command didn't work... try again! Type **-commands** for formatting rules")


@client.command()
async def show(ctx):
    try:
        showName = getShow().capitalize()
        json = get_json('tv', showName)['results'][0]
        poster= get_poster(json)
        providers=get_providers('tv',get_id(json))
        description = get_overview(json)
        prettyproviders=""
        for i in providers:
            if len(providers) > 1:
                prettyproviders+=i+',    '
            prettyproviders+= i
        embed = discord.Embed(title=showName, description=description, color=BLUE)
        embed.set_image(url = poster)
        if providers:
            embed.add_field(name="Currently Streaming On:", value=prettyproviders)
        else:
            embed.add_field(name="Not streaming anywhere :(", value="\u200b")
        await ctx.send(embed=embed)
    except:
        await ctx.send("command didn't work... try again! Type **-commands** for formatting rules")

@client.command()
async def game(ctx):
    try:
        await ctx.send(getGame().capitalize())
    except:
        await ctx.send("command didn't work... try again! Type **-commands** for formatting rules")

@client.command()
async def delmovie(ctx,*,arg):
    try:
        deleteMovie(arg)
        arg=arg.capitalize()
        await ctx.send(f"deleted {arg} from movie list")
    except:
        await ctx.send("command didn't work... try again! Type **-commands** for formatting rules")

@client.command()
async def delshow(ctx,*,arg):
    try:
        deleteShow(arg)
        arg=arg.capitalize()
        await ctx.send(f"deleted {arg} from show list")
    except:
        await ctx.send("command didn't work... try again! Type **-commands** for formatting rules")
    
@client.command()
async def delgame(ctx,*,arg):
    try:
        deleteGame(arg)
        arg=arg.capitalize()
        await ctx.send(f"deleted {arg} from game list")
    except:
        await ctx.send("command didn't work... try again! Type **-commands** for formatting rules")

@client.command()
async def addmovie(ctx,*,arg):
    try:
        addMovie(arg)
        arg=arg.capitalize()
        await ctx.send(f"added {arg} to movie list")
    except:
        await ctx.send("command didn't work... try again! Type **-commands** for formatting rules")

@client.command()
async def addshow(ctx,*,arg):
    try:
        addShow(arg)
        arg=arg.capitalize()
        await ctx.send(f"added {arg} to show list")
    except:
        await ctx.send("command didn't work... try again! Type **-commands** for formatting rules")

@client.command()
async def addgame(ctx,*,arg):
    try:
        addGame(arg)
        arg=arg.capitalize()
        await ctx.send(f"added {arg} to game list")
    except:
        await ctx.send("command didn't work... try again! Type **-commands** for formatting rules")

@client.command()
async def movielist(ctx):
    table = getTable('MOVIES')
    try:
        if len(table)==0:
            await ctx.send("No movies in list yet!")
        else:
            await ctx.send(formatList('MOVIES',table))
    except:
        await ctx.send("command didn't work... try again! Type **-commands** for formatting rules")

@client.command()
async def showlist(ctx):
    table = getTable('SHOWS')
    try:
        if len(table)==0:
            await ctx.send("No shows in list yet!")
        else:
            await ctx.send(formatList('SHOWS',table))
    except:
        await ctx.send("command didn't work... try again! Type **-commands** for formatting rules")

@client.command()
async def gamelist(ctx):
    table = getTable('GAMES')
    try:
        if len(table)==0:
            await ctx.send("No games in list yet!")
        else:
            await ctx.send(formatList('GAMES',table))
    except:
        await ctx.send("command didn't work... try again! Type **-commands** for formatting rules")


client.run(TOKEN)
