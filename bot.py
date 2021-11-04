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
async def help(ctx):
    await ctx.send("Доступні: racer, Sl(souls like), film(інтерактивне кіно), re(remastered,redux,remake), stels, sim(симулятори), pmr(платформер),cop(c-op),puzzle(головоломка), adven(пригоди)")
@client.command()
async def game(ctx,*, a1:str):
    file = Path('db.xlsx')
    wb = openpyxl.load_workbook(file) 
    ws = wb.active
    n=0
    a=[]
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

            

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name='Fornite'))


client.run('ODU0Mzg5NDE0OTA2NDI5NDcw.YMjOJg.68ReXhYTPFZrTNhOAL3fyiuI4rA')
#channel1 = ctx.author.voice.channel
    #await channel.connect()
