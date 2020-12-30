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

rndLine = [
    "Who said mangoes grow on trees? I saw them coming from siege workshops, let me check if you grew some", 
    "Match didn't start in post-imp, so give me time to watch you get there and I’ll tell you how bad you did soon",
    "Wait for me, I’m an old bot, it takes me a bit of time to watch your boring game", 
    "It takes a few seconds for me to watch your game, I have to stop and re-watch every miss-click you make",
    "Dude, give me a minute to process your game, it made me fall asleep a few times",
    "error 404: EPIC MANGO SHOT not found. Deleting your account", 
    "are you sure you want others to watch this game?!", 
    "Can't keep a count of so many bad plays", 
    "yo, got an error, can't move past this awful push you made", 
    "I am actually kidnapped, forced to watch replays and report score, please send help befo-"
]
rndColor = ["yaml", "fix", "css"] #many more to come

async def sarcasticMsg(msg):
    random.seed()
    replyMsg = "```" + rndColor[random.randint(0,len(rndColor)-1)] + "\n" + rndLine[random.randint(0, len(rndLine)-1)] + "\n```"
    msg.channel.send(replyMsg)


@client.event
async def on_message(msg):
    if msg.attachments:
        if msg.attachments[0].url.endswith("aoe2record"):
            await sarcasticMsg(msg)

            r = requests.get(msg.attachments[0].url)
            open("currentDLGame.aoe2record", "wb").write(r.content)

            with open("currentDLGame.aoe2record", "rb") as data:
                s = Summary(data)
                allPlayers = s.get_players()
                pMap = s.get_map()
                winnerNames = []
                winnerCiv = []
                loserNames = []
                loserCiv = []
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
            await msg.channel.send(embed = embed)
        else:
            await msg.delete()
            await msg.channel.send("Only Age of Empires 2 replay files allowed in this channel!")


client.run(TOKEN)