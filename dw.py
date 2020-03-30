import discord
from discord.ext import commands
import team
import random
import asyncio
import secrets

# Change the following line to change the bot's callword.
bot = commands.Bot(command_prefix='d ')
players = []
teams = []
timers = 1

@bot.command()
async def test(ctx):
    print(ctx)
    if ctx.author.dm_channel == None:
        await ctx.author.create_dm()
    await ctx.author.dm_channel.send("yo lemme test sliding into those dms")
    await ctx.send('testing decrypto bot')

@bot.command()
async def reset(ctx):
    global players, teams
    players = []
    teams = []
    await ctx.send("reset players. commit to playing next round by sending 'decrypto addme'")

@bot.command()
async def addme(ctx):
    global players
    if ctx.author in players:
        await ctx.send("%s is already in the game." % (str(ctx.author)))
        return
    players.append(ctx.author)
    await ctx.send("Added player %s to game. Player list: %s" % (str(ctx.author), ", ".join(str(p) for p in players)))

@bot.command()
async def startgamm(ctx):
    global players, teams
    if len(players) < 1:
        await ctx.send("Not enough players. %d players in: %s (four required)" % (len(players), str(players)))
        return
    else:
        teams = []
        random.shuffle(players)
        teams.append(team.Team(players=players[:len(players)//2], meme_bool=True))
        teams.append(team.Team(players=players[len(players)//2:], meme_bool=True))
        for p in players:
            if p.dm_channel == None:
                await p.create_dm()
        
        for t in teams:
            await t.send_welcome_messages()

@bot.command()
async def startgame(ctx):
    global players, teams
    if len(players) < 1:
        await ctx.send("Not enough players. %d players in: %s (four required)" % (len(players), str(players)))
        return
    else:
        teams = []
        random.shuffle(players)
        teams.append(team.Team(players=players[:len(players)//2]))
        teams.append(team.Team(players=players[len(players)//2:]))
        for p in players:
            if p.dm_channel == None:
                await p.create_dm()
        
        for t in teams:
            await t.send_welcome_messages()

@bot.command()
async def draw(ctx):
    global teams
    summary = await teams[0].send_draw()
    summary += " and "
    summary += await teams[1].send_draw()
    await ctx.send(summary)

@bot.command()
async def reveal(ctx):
    global teams
    for t in teams:
        if ctx.author in t.players:
            await t.reveal_draw(ctx)

@bot.command()
async def timer(ctx):
    global timers
    num = timers
    timers += 1
    name = str(ctx.author)
    await ctx.send("Starting a one minute timer for %s (timer %d)" % (name, num))
    await asyncio.sleep(60)
    await ctx.send("Timer for %s (%d) is complete" % (name, num))

@bot.command()
async def endgame(ctx):
    global teams
    msg = ""
    for t in teams:
        msg += "%s's team had the following words: %s\n" % (t.get_player_list(), t.get_words())
    await ctx.send(msg)

@bot.command()
async def h(ctx):
    msg = """Hi, and welcome to discrypto.

    For a notes cheat sheet, here's a gist: https://gist.github.com/aaravzen/ea17c20a735e7f43c540dccc2d405115

    For instructions on how to play, and to support the official game: https://www.scorpionmasque.com/en/decrypto

    This bot's commands are as follows ('d' is whatever callword you used to get this):
    - `d reset` - reset the game state
    - `d addme` - add a player to the game (must be sent by all players who want to be cluegivers)
    - `d startgame` - make teams and start the game (send out word info to players)
    - `d draw` - draws a card for a player on each team. Goes in a round robin fashion according to the list sent out to players at the start of the game.
    - `d reveal` - reveals the last draw for your team (will reveal cards that you didn't draw, will not reveal anything to players not on a team)
    - `d timer` - starts a one minute timer for the player (for when someone is done writing their clues)
    `d endgame` - will end the game and send a summary with all the round's words

    If you have any questions or comments, please keep those in mind as you enjoy playing discrypto. Thank you! ~Aarav"""
    await ctx.send(msg)
    


token = secrets.get_token()
bot.run(token)
