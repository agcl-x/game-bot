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
@client.command(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title='Help',description="{}-не потрібно писати", color=discord.Colour.purple())
    em.add_field(name = 'Ігри', value = '.game {щось небудь (назва, рік, розробник, або ключове слово(щось по типу жанру))}\nНа разі доступні ключові слова: racer, Sl(souls like), film(інтерактивне кіно), re(remastered,redux,remake), stels, sim(симулятори), pmr(платформер),cop(c-op),puzzle(головоломка), adven(пригоди)',inline=False)
    em.add_field(name = 'Спам', value = '.spam {к-ть повідомлень} , { фраза}',inline=False)
    em.add_field(name = 'Змінити статус', value = '.change_status - (Тільки для адміна)',inline=False)
    await ctx.send(embed = em)
@client.command()
async def spam(ctx, a1, *, a2):
    for i in range(0,int(a1)):
        await ctx.send(str(a2))
        time.sleep(0.7)
@client.event
async def on_voice_state_update(member:discord.Member, before, after):
    global voices
    guild= discord.utils.get(client.guilds, id=794363687497760770)
    for guild in client.guilds:
        mainc = discord.utils.get(guild.categories, id=794363687497760770)
    if before.channel is None and after.channel is not None:
        channelid1 = after.channel.id
        if channelid1 == 906466935271727144:
            chan = await guild.create_voice_channel(f'{member.name}party', category=mainc)
            await member.move_to(chan)
            voices.append(chan.id)
    if after.channel is None and before.channel is not None:
        for i in voices:
            channel = client.get_channel(i) #gets the channel you want to get the list from
            if channel is not None:   
                members = channel.members #finds members connected to the channel
                memids = [] #(list)
                for member in members:
                    memids.append(member.id)
                if memids==[]:
                    existing_channel = discord.utils.get(guild.channels, id=i)
                    await existing_channel.delete()
                    voices.remove(i) 
            else:
                print("loh") 
@client.command()
async def game(ctx,*, arg:str):
    file = Path('db.xlsx')
    wb = openpyxl.load_workbook(file) 
    ws = wb.active
    n=0
    a=[]
    a1=arg.lower()
    k=0
    mn=0
    for row in ws.values:
        n+=1
        main=list(row)
        if n>1:
            r_l=[str(i).lower() for i in main]
            #print(r_l)
            if r_l[0]!=None and r_l[1]!=None:
                dev=r_l[1]
                ganre=r_l[3]
                if ',' in ganre:
                    all_gan=r_l[3].replace(' ', '').split(',')                
                else:
                    all_gan=r_l[3]
                    
                if ',' in dev:
                    all_dev=r_l[1].replace(' ', '').split(',')
                else:
                    all_dev=r_l[1]
        #elif lst[0]==None or lst[1]==None:
            #print('.')
                name=r_l[0].replace(':', ' ').split(' ')
            #print(name)
                game = r_l[0]
                if (a1 in r_l) or (a1 in all_gan) or (a1 in all_dev) or (a1 in name):
                    a.append(n)
                    print(a)
        else:
            pass
    l=int(len(a))
    if l==1:
        for row in ws.values:
            k+=1
            if k == n:
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
@client.command
@commands.has_any_role("Admin GAY")
async def change_status(ctx,a1:str):
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name=a1))           

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name='Fornite'))


client.run('ODU0Mzg5NDE0OTA2NDI5NDcw.YMjOJg.68ReXhYTPFZrTNhOAL3fyiuI4rA')
#channel1 = ctx.author.voice.channel
    #await channel.connect()
