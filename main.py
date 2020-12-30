import os
import sys
import requests
import random
import discord
from dotenv import load_dotenv
sys.path.append(os.path.abspath("/mgzBaseFolder/mgz/summary"))
from mgz.summary import Summary

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

civCode = ["Britons", "Franks", "Goths", "Teutons", "Japanese", "Chinese", "Byzantines", "Persian", "Saracens", "Turks", "Vikings", "Mongols", "Celts", "Spanish", "Aztecs", "Mayans", "Huns", "Koreans", "Italians", "Indians", "Incas", "Magyars", "Slav", "Portuguese", "Ethiopians", "Malians", "Berbers", "Khmer", "Malay", "Burmese", "Vietnamese", "Bulgarians", "Tatars", "Cumans", "Lithuanians"]

randomLines = [
    "Who said mangoes grow on trees? They grow from siege workshops, let me check if you grew some", "Match didn't start in post-imp, so give me some time to watch you get there and I’ll tell you how bad you did soon.","Wait for me, I’m an old bot, it takes me a bit of time to watch your boring game.", "It takes a few seconds for me to watch your game, I have to stop and re-watch every miss-click you make.","Dude, give me a minute to process your game, it made me fall asleep a few times.","error 404: epic mango shot not found. Deleting your account", "are you sure you want others to watch this game?!", "ERROR 42069: Bad_Plays integer overflow", "Current game time: 1h6m24s - Current vill number: 69 - Idle time: indefinite", "I am actually kidnapped, to watch replays and report score, please send help befo-"
]

@client.event
async def on_message(msg):
    if msg.attachments:
        if msg.attachments[0].url.endswith("aoe2record"):
            random.seed()
            await msg.reply(randomLines[random.randint(0, len(randomLines))])

            r = requests.get(msg.attachments[0].url)
            open("currentDLGame.aoe2record", "wb").write(r.content)

            with open("currentDLGame.aoe2record", "rb") as data:
                s = Summary(data)
                allPlayers = s.get_players()
                #pSettings = s.get_settings()
                pMap = s.get_map()
                winnerNames = []
                winnerCiv = []
                loserNames = []
                loserCiv = []
                #endString = ""
                wTeam = ""
                lTeam = ""
            for x in allPlayers:
                if x["winner"]:
                    winnerNames.append(x["name"])
                    winnerCiv.append(civCode[x["civilization"]-1])
                else:
                    loserNames.append(x["name"])
                    loserCiv.append(civCode[x["civilization"]-1])
            for w in range(len(winnerNames)):
                wTeam += winnerNames[w] + " - " + winnerCiv[w] + "\n"
                lTeam += loserNames[w] + " - " + loserCiv[w] + "\n"
                #wCount = len(winnerNames[w] + "as *" + winnerCiv[w]+"*")
                #wSpace = " " * (40-wCount)
                #lCount = len(loserNames[w] + "as *" + loserCiv[w]+"*")
                #lSpace = " " * (40-lCount)
                #endString += "> " + winnerNames[w] + " - " + winnerCiv[w] + wSpace + "**:**" + lSpace + loserNames[w] + " - " + loserCiv[w] + "\n"

            #print("> Map: **" + str(pMap["name"]) + "**\n>" + "Score:" + " " * 25 + "Won" + " "*25 + "**:**" + 25*" " + "Lost" + 25*" " + "\n" + endString)
            
            #await msg.channel.send("> Map: **" + str(pMap["name"]) + "**\n>" + " "*25 + "Won" + " "*25 + "**-**" + " "*25 + "Lost" + " "*25 + "\n" + endString)
            embed = discord.Embed(title = "Map: ||" + str(pMap["name"]) + "||")
            if random.randint(0,1) == 1:
                embed.add_field(name = "Winner:", value = "||**Team 1**||", inline= False)
                embed.add_field(name = "Team 1", value = wTeam, inline = True)
                embed.add_field(name = "VS", value = "   -   \n"*len(winnerNames), inline = True)
                embed.add_field(name = "Team 2", value = lTeam, inline = True)
            else:
                embed.add_field(name = "Winner:", value = "||**Team 2**||", inline= False)
                embed.add_field(name = "Team 1", value = lTeam, inline = True)
                embed.add_field(name = "VS", value = "   -   \n"*len(winnerNames), inline = True)
                embed.add_field(name = "Team 2", value = wTeam, inline = True)
            await msg.reply(embed = embed)


client.run(TOKEN)