
#Discord imports
import discord
from discord.ext import commands
from discord import Spotify
from discord.ext.commands import MemberConverter
from discord import Emoji

#python libraries
import os
import sys
import time
import asyncio
import urllib.parse
import json

import argparse
from collections import defaultdict

#Google imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("./otherFiles/creds.json")
gsheet = gspread.authorize(creds)
sheet = gsheet.open('Discord Data').sheet1
sheet2 = gsheet.open('Discord Data').get_worksheet(1) #0 is to 1, 1 is to 2, and so on

#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
#pip install discord.py
#pip install pynacl
#pip install discord.py[voice]
#pip install gspread oauth2client

#if youtube_dl doesnt work:
#cd C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\
#python.exe -m pip install youtube_dl
#-m pip install pynacl

#C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\python.exe

#FOR INITIALIZING GIT AND HEROKU
#git init
#git commit -am "hi"
#git add .
#git push heroku master

#https://www.youtube.com/watch?v=qjtmgCb8NcE << YT Tutorial for ffmpeg


client = commands.Bot(command_prefix = '!') #for commands :) ex. !play on ry thm


x = 0

xtoken = open("./otherFiles/token.txt")
for numbers in xtoken:
    token = numbers

#@client.command()
#async def load (ctx, extension):
#    client.load_extension(f'cogs.{extension}')  #goes into the cogs folder and looks for the cogs
#@client.command()
async def unload (ctx, extension):
    client.unload_extension(f'cogs.{extension}')  #goes into the cogs folder and looks for the cogs

@client.event #function decorator denoting that function is representing an event
async def on_ready(): #runs when the bot is ready
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="LOFI HipHop"))
    #if discord.id(x) == 354180424496447489:
        #await ctx.send('UwU')
    print('Bot is up!')


async def nickchange(member: discord.Member, nick): #changes nickname
    await member.edit(nick = nick)
    await member.send(f'Nickname was changed for {member.mention}. Your nickname is: {nick}')


@client.event
async def on_member_join(member): #TODO: autoassign a nickname
    global nicknames, plate_num
    print(f'{member} has joined a server.') #says everytime someone has joined a server


@client.event
async def on_member_remove(member): #when someone leaves or gets kicked from the server
    print(f'{member} has left a server.')

@client.command()
async def ping(ctx):
    """Check bot ping"""
    await ctx.send(f'Pong! {round(client.latency *1000)} ms')




converter = MemberConverter() #Converts string to discord.member
oldSong = None
myName = 'Lunaria#3150'
user = None

newSong = None
dm_channel = None
message = None
fixed_channel = None

grade = None
strand = None

grade11 = int(sheet2.cell(2,1).value)
grade12 = int(sheet2.cell(2,2).value)

gradex = None
tempdict = dict()
memberlist = dict()
gtempdict = dict()
stempdict = dict()
templist = list()
@client.command()
async def startup(ctx): #TODO: make it set custom nicknames ;)
#Register as new User (not yet implemented properly)

    global user, oldSong, newSong, dm_channel, message, fixed_channel
    fixed_channel = ctx.channel
    print(f'fixed_channel = {fixed_channel}')

    emojis = ['<:G11:780793337107185664>', '<:G12:780793377922482188>']
    botmessage = await ctx.send("""
    HELLO! To proceed with the experiment, please click the <:G11:780793337107185664> icon below this text if you are in the Grade 11 Batch, and <:G12:780793377922482188> icon if you are in the Grade 12 Batch.
    """)
    #await continuation()
    for emoji in emojis:
        await botmessage.add_reaction(emoji)

    await continuation()

    message = ctx
    user = ctx.author
    userid = f'<@{ctx.author.id}>'
    #await ctx.send(f'Thank you for registering {userid}! Your id is {x}')

async def continuation():
    global fixed_channel
    emojis = ['🟩','🟦','🟧','🟥','🟨']
    message = await fixed_channel.send("""
    Please click the respective icon for below this text your strand:
    🟩 for **STEM**,
    🟦 for **ABM**,
    🟧 for **HUMSS**,
    🟥 for **ADT**, and
    🟨 for **SPT**
    """)
    for emoji in emojis:
        await message.add_reaction(emoji)
    await fixed_channel.send('And to finalize, please enter the command "!register" in the channel "#section" with your section.. \n ✅ Example: !register C')


@client.event
async def on_reaction_add(reaction, user):
    global grade, strand, fixed_channel, grade11, grade12, sheet2, gradex, memberlist,tempdict,templist
    emoji = reaction.emoji
    if user.bot:
        return
    gtempdict = dict()
    stempdict = dict()

    if isinstance(emoji, Emoji):
        if emoji.name == 'G11':
            gtempdict = {'Grade':11}

        elif emoji.name == 'G12':
            gtempdict = {'Grade':12}


    if emoji == '🟩':
        stempdict = {'Strand': 'STEM'}
    elif emoji == '🟦':
        stempdict = {'Strand': 'ABM'}
    elif emoji == '🟧':
        stempdict = {'Strand': 'HUMSS'}
    elif emoji == '🟥':
        stempdict = {'Strand': 'ADT'}
    elif emoji == '🟨':
        stempdict = {'Strand': 'SPT'}

    #if user.id not in memberlist.keys():
    #tempdict = {user.id:{gtempdict, stempdict}}

    userid = user.id
    stemp = stempdict
    gtemp = gtempdict

    if userid in memberlist.keys():
        if len(gtempdict) != 0:
            for i, mx in enumerate(memberlist[user.id]):
                if 'Grade' in mx:
                    del memberlist[user.id][i]
                    memberlist[userid].insert(0,gtempdict)
                    print(memberlist, 'in memberlist')
                    break
            else:
                memberlist[userid].insert(0,gtempdict)
                print(memberlist, 'not in memberlist')


        if len(stempdict) != 0:
            for i,mx in enumerate(memberlist[user.id]):
                if 'Strand' in mx:
                    del memberlist[user.id][i]
                    memberlist[userid].insert(1,stempdict)
                    print(memberlist)
                    break
            else:
                memberlist[userid].insert(1,stempdict)
                print(memberlist)

    elif userid not in memberlist:
        tempdict = {userid:list()}
        memberlist.update(tempdict)
        if len(gtempdict) != 0:
            memberlist[userid].insert(0,gtempdict)
            print(memberlist)
        if len(stempdict) != 0:
            memberlist[userid].insert(1,stempdict)
            print(memberlist)



@client.command()
async def register(ctx, section):
    global strand,grade,grade12,sheet2, grade11, gradex, memberlist
    user = ctx.author
    if user.id not in memberlist:
        await ctx.send("Please go back to the previous channel and react to the Grade and Strand Selection")
    else:
        try:
            testing = memberlist[user.id][0]['Grade']
            testing2 = memberlist[user.id][1]['Strand']
        except:
            await ctx.send('You missed something. Please go back to the previous channel and re-check.')
            return
        if memberlist[user.id][0]['Grade'] == 11:
            gradex = int(sheet2.cell(2,1).value)
            gradex += 1
            sheet2.update_cell(2,1, gradex)
        elif memberlist[user.id][0]['Grade'] == 12:
            gradex = int(sheet2.cell(2,2).value)
            gradex += 1
            sheet2.update_cell(2,2, gradex)

        #Group Number Change
        group_number = (gradex//10) + 1
        group = discord.utils.get(ctx.guild.roles, name = f'GROUP {group_number}')
        await user.add_roles(group)

        if (gradex%2) == 0:
            try:
                role = discord.utils.get(ctx.guild.roles, name = 'EXPERIMENTAL GROUP')
                await user.add_roles(role)
            except:
                guild = ctx.guild
                await guild.create_role(name = 'EXPERIMENTAL GROUP', hoist = True)
                role = discord.utils.get(ctx.guild.roles, name = 'EXPERIMENTAL GROUP')
                await user.add_roles(role)
        elif ((gradex)%2) != 0:
            try:
                role = discord.utils.get(ctx.guild.roles, name = 'CONTROLLED GROUP')
                await user.add_roles(role)
            except:
                guild = ctx.guild
                await guild.create_role(name = 'CONTROL GROUP', hoist = True)
                role = discord.utils.get(ctx.guild.roles, name = 'CONTROLLED GROUP')
                await user.add_roles(role)


        await nickchange(ctx.author, nick = f"[{memberlist[user.id][1]['Strand']} {memberlist[user.id][0]['Grade']}-{section}] #{gradex}")


    #grade12 = int(sheet2.cell(2,2).value)



@client.command()
async def resetid(ctx, message):
    try:
        intmessage = int(message)
    except:
        intmessage = -1
    if ctx.author.id == 378032399327690754:
        if intmessage != -1:
            await ctx.send(f'ID has been reset to: {message}')
            sheet2.update_cell(2,1, message)
            sheet2.update_cell(2,2, message)
    else:
        await ctx.send('Access to this command has been denied.')
#=============================Spotify Detector========================================================

@client.event
async def on_member_update(before, after):
    global user, oldSong, newSong
    #print(after.id)
    for activity in after.activities:
        xactivity = str(activity) #retard python cant run the dumbass if statement if it isnt a string
        if xactivity == 'Spotify': #TODO: include in parameters: a list of discord ids of respondents ;)
            print('========================================================================================')
            print('Nickname: ',after.nick) #TODO: Add an if nickname == None parameter
            print('Song: ',activity.title)
            print('Time: ', time.asctime())
            songlog = [str(after.nick), str(after.name), str(activity.title), str(time.asctime())]
            #json_string = json.dumps(songlog)
            sheet.insert_row(songlog, 2)
            songlog.clear()
            #with open(f'./data_gathered/{after.nick}.txt', 'a', encoding = 'utf-8') as f: #TODO: seperate into folders (per server ;) or new row if im gonna do databases
            #    f.write(f'Time: {time.asctime()}, Song: {activity.title}\n')
            #    f.close()

#========================================================================================================

#@client.event
#async def on_message(message):
#    if message.content == 'hi':
#        await message.add_reaction('<:pepe:780788372692008980>')


#detects Allain's id and sends a message lmfaooo
#@client.event
#async def on_message (message):
#    channel = message.channel
#    if message.author.id == 354180424496447489:
#        await channel.send('FUCK YOU AND YOUR ELDERWOOD LEB')
#
#    await client.process_commands(message) #bot ignores commands and only executes on_message without this line
#for filename in os.listdir('./cogs'): #loops for all the files and checks if its a py file
#    if filename.endswith('.py'):
#        client.load_extension(f'cogs.{filename[:-3]}') #removes the last 3 charactes (also loads the thingy)



client.run(token) #token (private shit cus other people can control ur shit when they have this)
