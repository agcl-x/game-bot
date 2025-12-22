import discord, openpyxl, random
from discord.ext import commands
from discord import app_commands
from pathlib import Path
from discord.ui import View
import config
import difflib

def isint(x):
    try:
        int(x)
        return True
    except Exception:
        return False
def isfloat(x):
    try:
        float(x)
        if isint(x):
            return False
        else:
            return True
    except Exception:
        return False
def most_similar_string(input_string, list_of_strings):
    closest_match = difflib.get_close_matches(input_string, list_of_strings, n=1)
    return closest_match[0] if closest_match else None

voices=[]
voices_created=[]
client = commands.Bot(command_prefix= config.prefix, intents = discord.Intents.all())
client.remove_command("help")

db_file = Path('db.xlsx')
db = openpyxl.load_workbook(db_file).active
list_of_names=[]
list_of_genre=[]
temp_ln=3
ln=1
bl=True
for row in db.values:
    r_l=[str(i) for i in list(row)]
    if ln>3:
        list_of_names.append(r_l[0])
        list_of_genre.append(r_l[3])
    if r_l[0] == str(None) and bl:
        bl=False
        temp_ln=ln
    if ln-1==temp_ln and r_l[0] == str(None):
        break
    elif ln-1!=temp_ln and r_l[0] == str(None):
        temp_ln=ln
    ln+=1

class Buttons(discord.ui.Button):
    def __init__(self, label, style,page,user_id):
        super().__init__(label=label, style=style)
        self.message_content=page
        self.user_id=user_id
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id==self.user_id:
            await interaction.response.edit_message(embed=self.message_content)

def embed_writer(dictionary, embed):
    for i in dictionary:
        string=""
        element=dictionary[i]
        if str(type(element))=="<class 'dict'>":
            for j in element:
                if element[j]!="!":
                    string+=f"{j}:  *{element[j]}*\n"
        else:
            string=element
        embed.add_field(name = i.upper(), value = string , inline=False)
    return embed

def check_if_not_undefined(dictionary):
    to_delete={}
    for i in dictionary:
        if str(type(dictionary[i]))=="<class 'dict'>":
            for j in dictionary[i]:
                if dictionary[i][j] == "?":
                    to_delete[i]=j
                elif dictionary[i][j] == "/?":
                    dictionary[i][j] = "?"
            for j in to_delete:
                dictionary[j].pop(to_delete[j])
            to_delete={}
        else:
            if dictionary[i]=="?":
                dictionary[i].pop(i)
            elif dictionary[i] == "/?":
                dictionary[i] = "?"
    return dictionary

@client.tree.command(name="game")
@app_commands.describe(genre="Жанр гри", age_from="Пошук від якогось року", age_to="Пошук до якогось року", name="Назва гри")
async def game(interaction: discord.Interaction,genre:str=None, age_from:int=None, age_to:int=None,*, name:str=None):
    temp_list_of_names=list_of_names[:]
    temp_list_of_genre=list_of_genre[:]
    list_of_finded=[]
    if name:
        print(name)
        most_similar=most_similar_string(name, temp_list_of_names)
        while most_similar:
            temp_list_of_names.remove(str(most_similar))
            list_of_finded.append(list_of_names.index(str(most_similar))+4)
            most_similar=most_similar_string(name, temp_list_of_names)
    elif genre:
        print(genre)
        most_similar=most_similar_string(genre, temp_list_of_genre)
        while most_similar:
            temp_list_of_genre.remove(most_similar)
            list_of_finded.append(list_of_genre.index(most_similar)+4)
            most_similar=most_similar_string(genre, temp_list_of_genre)
    print(list_of_finded)
    if len(list_of_finded)!=0:
        index=random.choice(list_of_finded)
        print(index)
        await interaction.response.defer()
    else:
        await interaction.response.defer()
        await interaction.followup.send("Game not found")
    print("for")
    cn=1
    for row in db.values:
        print(cn)
        r_l=[str(i) for i in list(row)]
        if cn==index:
            print("ok1")
            if age_from:
                if int(float(r_l[2]))<age_from:
                    continue
            if age_to:
                print("age_to")
                if int(float(r_l[2]))>age_to:
                    continue
            print(r_l)
            print("embed forming")
            about={"About":{"Developer":r_l[1],"Year":int(float(r_l[2])),"Genre":r_l[3]},"Metacritic":{"Critic":None,"User":None}}
            min_req={"cpu":{"Intel":str(r_l[10]),"AMD":str(r_l[11])},"gpu":{"Intel":str(r_l[14]),"AMD":str(r_l[13]),"NVIDIA":str(r_l[12])},"ram":str(r_l[15]),"storage":str(r_l[6]), "os":{"Windows":str(r_l[7]),"Linux":str(r_l[8]),"Mac OS":str(r_l[9])}}
            max_req={"cpu":{"Intel":str(r_l[16]),"AMD":str(r_l[17])},"gpu":{"Intel":str(r_l[20]),"AMD":str(r_l[19]),"NVIDIA":str(r_l[18])},"ram":str(r_l[21]),"storage":str(r_l[6]), "os":{"Windows":str(r_l[7]),"Linux":str(r_l[8]),"Mac OS":str(r_l[9])}}
            link={"dwn":r_l[22],"poster":r_l[23],"steam":r_l[24]}
            name=r_l[0]
            if isint(r_l[4]):
                about["Metacritic"]["Critic"]=int(float(r_l[4]))
            else:
                about["Metacritic"]["Critic"]=r_l[4]
            if isfloat(r_l[5]):
                about["Metacritic"]["User"]=float(r_l[5])
            else:
                about["Metacritic"]["User"]=r_l[5]
            min_req=check_if_not_undefined(min_req)
            max_req=check_if_not_undefined(max_req)
            about=check_if_not_undefined(about)
            em_main = discord.Embed(title=f"**{name}**", description = f'Download link:{link["dwn"]}', color=discord.Colour.purple())
            em_min=discord.Embed(title=name, description = 'Minimum system requirments', color=discord.Colour.purple())
            em_max=discord.Embed(title=name, description = 'Recommended system requirments', color=discord.Colour.purple())
            em_main.set_image(url=f'{link["poster"]}')
            em_min.set_image(url=f'{link["poster"]}')
            em_max.set_image(url=f'{link["poster"]}')
            embed_writer(min_req,em_min)
            embed_writer(max_req,em_max)
            embed_writer(about,em_main)    

            button_main=Buttons("Main",discord.ButtonStyle.primary,em_main,interaction.user.id)
            button_min=Buttons("Min",discord.ButtonStyle.primary,em_min,interaction.user.id)
            button_max=Buttons("Max",discord.ButtonStyle.primary,em_max,interaction.user.id)
            view = View()
            view.add_item(button_main)
            view.add_item(button_min)
            view.add_item(button_max)
            await interaction.followup.send(embed = em_main, view=view)
            break
        cn+=1

@client.command()
async def party(ctx,*, a):
    global voices
    try:
        b=a.replace("<","").replace(">","")
        list_of_added=b.replace(" ","").split("@")
        del list_of_added[0]
    except Exception:
        await ctx.reply('Неправильно введені користувачі')
    for guild in client.guilds:
        mainc = discord.utils.get(guild.categories, id=config.party_category_id)
    if ctx.author.voice == None:  
        await ctx.send('Зайди в любий войс чат')
    elif ctx.author.voice != None:
        party_voice = await guild.create_voice_channel(f'@{ctx.author.name} party', category=mainc)
        await ctx.author.move_to(party_voice)
        if len(list_of_added)>=1:
            for i in list_of_added:
                user = await ctx.bot.fetch_user(i)
                await party_voice.set_permissions(user, connect=True)
                await party_voice.set_permissions(ctx.guild.default_role, connect=False)
                await user.send(f'Привітики батончики. Тебе запросили в войс!\nhttps://discord.com/channels/{config.server_id}/{party_voice.id}')
            await ctx.reply('Запрошення надіслані. Очікуйте!')
        else:
            pass
        voices.append(party_voice.id)
@client.command()
async def add(ctx,*, a):# NEED TO BE FINISHED
    global id_m, channel, voices
    m=[]
    try:
        b=a.replace("<","").replace(">","")
        list_of_added=b.replace(" ","").split("@")
        del list_of_added[0]
    except Exception:
        await ctx.reply('Неправильно введені користувачі')
    if str(type(voices[ctx.author.voice.id]))=="<class 'list'>":
        m=voices[ctx.author.voice.id]
        for i in list_of_added:
            m.append(i)
    else:
        m.append(voices[ctx.author.voice.id])
        for i in list_of_added:
            m.append(i)
    voices[ctx.author.voice.id]=m
@client.command()
async def report(ctx,*,string):
    bot_developer=client.get_user(config.bot_dev_id)
    await bot_developer.send(f"Report from <@{ctx.author.id}:\n\t{string}")

@client.command()
@commands.has_any_role(config.admin_role_id)
async def change_status(ctx,a1:str):
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name=a1))           

@client.event
async def on_voice_state_update(member:discord.Member, before, after):
    global voices,voices_created
    guild= discord.utils.get(client.guilds, id=config.server_id)
    for guild in client.guilds:
        mainc = discord.utils.get(guild.categories, id=config.voice_category_id)
    if after.channel:
        channelid1 = after.channel.id
        if channelid1==config.voice_create_voices_id:
            chan = await guild.create_voice_channel(f'{member.name} voice', category=mainc)
            await member.move_to(chan)
            voices_created.append(chan.id)
    if before.channel is not None:
        channelid2 = before.channel.id
        members = before.channel.members
        if members ==[]:
            if channelid2 in voices_created:
                existing_channel = discord.utils.get(guild.channels, id=channelid2) #name=f'{member.name} party')
                await existing_channel.delete()  
            elif channelid2 in voices:
                voices.remove(channelid2)
                existing_channel = discord.utils.get(guild.channels, id=channelid2) #name=f'{member.name} party')
                await existing_channel.delete()

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name=config.activity))
    await client.tree.sync()

client.run(config.token)