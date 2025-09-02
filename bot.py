import discord, openpyxl, random
from discord.ext import commands
from pathlib import Path
import config

tempVoiceCounter=0
initiatorIDToInvitedID={}
initiatorIDToTempVoiceID = {}
tempVoiceIDsList=[]

xlsxDB = Path('db.xlsx')
workbook = openpyxl.load_workbook(xlsxDB)
worksheet = workbook.active

client = commands.Bot(intents = discord.Intents.all(), command_prefix= config.prefix)
client.remove_command("help")

for guild in client.guilds:
    tempVoicesCategory = discord.utils.get(guild.categories, id=config.tempVoicesCategoryID)

@client.command(invoke_without_command=True)
async def help(ctx):
    helpEmbed = discord.Embed(title='Help',description="{}-не потрібно писати", color=discord.Colour.purple())
    helpEmbed.add_field(name = 'Ігри', value = '.game {щось небудь (назва, рік, розробник, або ключове слово(щось по типу жанру))}\nНа разі доступні ключові слова: racer, Sl(souls like), film(інтерактивне кіно), re(remastered,redux,remake), stels, sim(симулятори), pmr(платформер),cop(c-op),puzzle(головоломка), adven(пригоди)',inline=False)
    helpEmbed.add_field(name = 'Спам', value = '.spam {к-ть повідомлень} , { фраза}',inline=False)
    helpEmbed.add_field(name = 'Змінити статус', value = '.change_status - (Тільки для адміна)',inline=False)
    await ctx.send(embed = helpEmbed)
@client.command()
async def party_accept(ctx):
    authorID=str(ctx.author.id)
    if authorID in initiatorIDToInvitedID and ctx.author.voice !=None:
        targetInitiatorID = None
        for initiatorID, invitedID in initiatorIDToInvitedID.items():
            if invitedID == authorID:
                targetInitiatorID = initiatorID
                break
        targetVoiceID = initiatorIDToTempVoiceID[targetInitiatorID]
        targetVoice = ctx.guild.get_channel(targetVoiceID)
        await ctx.reply('*_Тепер ти в паті!!_*')
        await ctx.author.move_to()
        await targetVoice.set_permissions(ctx.guild.default_role, connect=False)
    elif ctx.author.voice == None:
        await ctx.send('Зайди в любий войс чат')
    elif authorID not in initiatorIDToInvitedID:
        await ctx.send('Тебе ніхто не запрошував!')   
@client.command()
async def party(ctx, invitedToParty:discord.Member):
    global tempVoiceCounter, tempVoiceIDsList, initiatorIDToInvitedID, initiatorIDToTempVoiceID
    if ctx.author.voice == None:  
        await ctx.send('Зайди в любий войс чат')
    elif ctx.author.voice != None:
        tempVoiceCounter += 1
        newTempVoice = await guild.create_voice_channel(f'party{tempVoiceCounter}', category=tempVoicesCategory)
        tempVoiceIDsList.append(newTempVoice.id)
        initiatorIDToInvitedID[ctx.author.id] = invitedToParty.id
        initiatorIDToTempVoiceID[ctx.author.id] = newTempVoice.id
        await ctx.author.move_to(newTempVoice)
        await invitedToParty.send('Привіт! Тебе запросили в войс!')
        await ctx.reply('Запрошення надіслане. Очікуйте!')

@client.event
async def on_voice_state_update(member:discord.Member, before, after):
    if after.channel is None and before.channel is not None:
        currentTempVoiceID = before.channel.id
        currentTempVoice = client.get_channel(currentTempVoiceID)
        membersInTempVoice = currentTempVoice.members
        membersInTempVoiceID = []
        for member in membersInTempVoice:
            membersInTempVoiceID.append(member.id)
        if membersInTempVoiceID==[]:
            initiatorIDToTempVoiceID.remove(member.id)
            initiatorIDToInvitedID.remove(member.id)
            for voice in tempVoiceIDsList:
                existing_channel = discord.utils.get(tempVoicesCategory.channels, id = voice)
                await existing_channel.delete() 

@client.command()
async def game(ctx, *, userRequest: str):
    userRequest = userRequest.lower().strip()
    appropriateRows = []
    rowCounter = 0
    for row in worksheet.values:
        rowCounter += 1
        if rowCounter > 1:
            rowInList = [str(i).lower() if i is not None else "" for i in row]
            gameName = rowInList[0]
            gameDevs = rowInList[1].replace(" ", "").split(",")
            gameGanres = rowInList[3].replace(" ", "").split(",")

            if (userRequest in gameName or
                userRequest in gameDevs or
                userRequest in gameGanres or
                userRequest in gameName.replace(":", " ").split()):
                appropriateRows.append(row)

    if not appropriateRows:
        await ctx.send("Нічого не знайдено")
        return

    if len(appropriateRows) == 1:
        targetRow = appropriateRows[0]
    else:
        targetRow = random.choice(appropriateRows)

    year = str(targetRow[2])[:4]
    gameEmbed = discord.Embed(
        title=f"Your game is {row[0]}",
        description=f"Download link: {row[13]}",
        color=discord.Colour.purple()
    )
    gameEmbed.set_image(url=f"{row[14]}")
    gameEmbed.add_field(name="About", value=f"Year: {year}\nDeveloper: {row[1]}", inline=False)
    gameEmbed.add_field(name="Min", value=f"OS: {row[7]}\nCPU: {row[5]}\nGPU: {row[6]}\nRAM: {row[4]}\nFree place: {row[8]}", inline=False)
    gameEmbed.add_field(name="Max", value=f"OS: {row[12]}\nCPU: {row[10]}\nGPU: {row[11]}\nRAM: {row[9]}\nFree place: {row[8]}", inline=False)

    await ctx.send(embed=gameEmbed)



@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name=config.gameName))


client.run(config.token)
