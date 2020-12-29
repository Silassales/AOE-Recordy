import os
import requests
import random
import discord
from dotenv import load_dotenv
from mgz.summary import Summary

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

civCode = ["Britons", "Franks", "Goths", "Teutons", "Japanese", "Chinese", "Byzantines", "Persian", "Saracens", "Turks", "Vikings", "Mongols", "Celts", "Spanish", "Aztecs", "Mayans", "Huns", "Koreans", "Italians", "Indians", "Incas", "Magyars", "Slav", "Portuguese", "Ethiopians", "Malians", "Berbers", "Khmer", "Malay", "Burmese", "Vietnamese", "Bulgarians", "Tatars", "Cumans", "Lithuanians"]

@client.event
async def on_message(msg):
    if msg.attachments:
        if msg.attachments[0].url.endswith("aoe2record"):
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
            random.seed()
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


client.run(TOKEN)