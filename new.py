import time , discord, openpyxl, random
from discord.ext import commands
info={}

client = commands.Bot(command_prefix= str(pr) )
client.remove_command("help")
connection = pymysql.connect(host='167.71.38.226',
                             user='test',
                             password='test',
                             db='gamebot',
                             port=3306,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

def search_by_name_random(request:str):
	global info

	right=[]
	sql = f"""SELECT * FROM `id_name` WHERE 1"""
	cursor.execute(sql)
	result = cursor.fetchall()
	for dictionary in result:
		name_to_lower=dictionary['name'].lower()
		if request.lower() in name_to_lower:
			right.append(dictionary['id'])
	if len(right)!=0:
		final=choice(right)
	sql = f"""SELECT `name` FROM `id_name` WHERE `id`={final}"""
	cursor.execute(sql)
	info["name"] = cursor.fetchall()["name"]
	get_main_info_by_id(final)
	get_genre_by_id(final)
	get_minsys_by_id(final)
	get_recsys_by_id(final)
	get_links_by_id(final)
	get_scores_by_id(final)
def get_main_info_by_id(request):
	global info

	sql = f"""SELECT * FROM `id_info` WHERE `id`={request}"""
	cursor.execute(sql)
	info["year"] = cursor.fetchall()["year"]
	info["dev"] = cursor.fetchall()["dev"]

def get_minsys_by_id(request):
	global info

	sql = f"""SELECT * FROM `id_minsys` WHERE `id`={request}"""
	cursor.execute(sql)
	sys=cursor.fetchall()[0]
	info["cpu"] = sys["cpu"]
	info["gpu"] = sys["gpu"]
	info["ram"] = sys["ram"]
	info["rom"] = sys["rom"]
	info["os"] = sys["os"]
def get_recsys_by_id(request):
	global info

	sql = f"""SELECT * FROM `id_recsys` WHERE `id`={request}"""
	cursor.execute(sql)
	sys=cursor.fetchall()[0]
	info["cpu"] = sys["cpu"]
	info["gpu"] = sys["gpu"]
	info["ram"] = sys["ram"]
	info["rom"] = sys["rom"]
	info["os"] = sys["os"]

def get_links_by_id(request):
	global info

	sql = f"""SELECT * FROM `id_links` WHERE `id`={request}"""
	cursor.execute(sql)
	sys=cursor.fetchall()[0]
	info["torrent"] = sys["torrent"]
	info["photo"] = sys["photo"]

def get_genre_by_id(request):
	global info

	sql = f"""SELECT * FROM `id_genre` WHERE `id`={request}"""
	cursor.execute(sql)
	sys=cursor.fetchall()[0]
	info["genre"] = sys["genre1"]+","+sys["genre2"] 
def get_scores_by_id(request):
	global info

	sql = f"""SELECT * FROM `id_scores` WHERE `id`={request}"""
	cursor.execute(sql)
	sys=cursor.fetchall()[0]
	info["userscore"] = sys["userscore"]
	info["metascore"] = sys["metascore"] 
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name='Fornite'))

client.run('ODU0Mzg5NDE0OTA2NDI5NDcw.YMjOJg.68ReXhYTPFZrTNhOAL3fyiuI4rA')
#channel1 = ctx.author.voice.channel
    #await channel.connect()
