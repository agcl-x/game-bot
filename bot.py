import time , discord, openpyxl, random
from discord.ext import commands
from pathlib import Path
ch=0
pr='.'
n=[]
k=[]
sd=[]
kik=0
voices=[]
client = commands.Bot(command_prefix= str(pr) )
client.remove_command("help")
@client.command()
async def party_ac(ctx):
    global id, n, k, sd, channel,voices,kik
    auth=str(ctx.author.id)
    for i in voices:
        channel = client.get_channel(int(i)) #gets the channel you want to get the list from
        members = channel.members 
        memids = [] #(list)
        for member in members:
            memids.append(member.id)
    if auth in n and ctx.author.voice !=None:
        await ctx.reply('*_Тепер ти в паті!!_*')
        for i in sd:
            channel = client.get_channel(int(i)) 
            members = channel.members
            for j in k:
                if j in members:
                    kik+=1
                    await ctx.author.move_to(channel)
                    await channel.set_permissions(ctx.guild.default_role, connect=False)
    elif ctx.author.voice == None:
        await ctx.send('Зайди в любий войс чат')
    elif auth not in n:
        await ctx.send('Тебе ніхто не запрошував!')   
@client.command()
async def party(ctx, a1:discord.Member):
    global id, sd, k, ch, channel, n, voices
    #messages
    #lists
    id = str(a1.id)
    ch+=1
    n.append(id)
    k.append(ctx.author)
    for guild in client.guilds:
        mainc = discord.utils.get(guild.categories, id=855389853134225408)
    if ctx.author.voice == None:  
        await ctx.send('Зайди в любий войс чат')
    elif ctx.author.voice != None:
        await a1.send('Привітики батончики. Тебе запросили в войс!')
        await ctx.reply('Запрошення надіслане. Очікуйте!')
        chan = await guild.create_voice_channel(f'party{ch}', category=mainc)
        await ctx.author.move_to(chan)
        sd.append(str(chan.id))
        voices.append(str(chan.id))
@client.event
async def on_voice_state_update(member:discord.Member, before, after):
    if before.channel is None and after.channel is not None:
        print('.')
    if after.channel is None and before.channel is not None:
        channelid2 = before.channel.id
        channel = client.get_channel(channelid2) #gets the channel you want to get the list from
        members = channel.members #finds members connected to the channel
        memids = [] #(list)
        for member in members:
            memids.append(member.id)
        if memids==[]:
            for i in voices:
                existing_channel = discord.utils.get(guild.channels, id=int(i))
                await existing_channel.delete() 

@client.command()
async def game(ctx,*, a1:str):
    file = Path('db.xlsx')
    wb = openpyxl.load_workbook(file) 
    ws = wb.active
    n=0
    a=[]
    k=0
    for row in ws.values:
        n+=1
        lst=list(row)
        if lst[0]!=None and lst[1]!=None:
            print(lst[1])
            lstt=list(lst[1])
            lst2=list(lst[3])
            #print(lst2)
            
            if ',' in lst2:
                lst4=lst[3].replace(' ', '').split(',')
                
            else:
                lst4=lst[3]
                
            if ',' in lstt:
                lst1=lst[1].replace(' ', '').split(',')
            else:
                lst1=lst[1]
            if a1 in lst1 or a1 in row or a1 in lst4:
                a.append(n)
        elif lst[0]==None or lst[1]==None:
            print('.')
    l=int(len(a))
    if l==1:
        for row in ws.values:
            k+=1
            if k == ap:
                year=str(row[2])
                y=year[0]+year[1]+year[2]+year[3]
                em = discord.Embed(title='Your game is %s'%row[0], description = f'Download link:{row[13]}', color=discord.Colour.purple())
                em.set_image(url=f'{row[14]}')
                em.add_field(name = 'About', value = f'Year: {y}\nDeveloper: {row[1]}', inline=False)
                em.add_field(name = 'Min', value = f'OS:{row[7]}\nCPU:{row[5]}\nGPU:{row[6]}\nRAM:{row[4]}\nFree place:{row[8]}', inline=False)
                em.add_field(name = 'Max', value = f'OS:{row[12]}\nCPU:{row[10]}\nGPU:{row[11]}\nRAM:{row[9]}\nFree place:{row[8]}', inline=False)
                await ctx.send(embed = em)
    if l>1:
        rannum=random.randint(0, l)
        ap=a[rannum]
        for row in ws.values:
            k+=1
            if k == ap:
                year=str(row[2])
                y=year[0]+year[1]+year[2]+year[3]
                em = discord.Embed(title='Your game is %s'%row[0], description = f'Download link:{row[13]}', color=discord.Colour.purple())
                em.set_image(url=f'{row[14]}')
                em.add_field(name = 'About', value = f'Year: {y}\nDeveloper: {row[1]}', inline=False)
                em.add_field(name = 'Min', value = f'OS:{row[7]}\nCPU:{row[5]}\nGPU:{row[6]}\nRAM:{row[4]}\nFree place:{row[8]}', inline=False)
                em.add_field(name = 'Max', value = f'OS:{row[12]}\nCPU:{row[10]}\nGPU:{row[11]}\nRAM:{row[9]}\nFree place:{row[8]}', inline=False)
                await ctx.send(embed = em)

            

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name='Fornite'))


client.run('ODU0Mzg5NDE0OTA2NDI5NDcw.YMjOJg.68ReXhYTPFZrTNhOAL3fyiuI4rA')
#channel1 = ctx.author.voice.channel
    #await channel.connect()