#import openpyxl
#from pathlib import Path
import pymysql
#file = Path('db.xlsx')
#wb = openpyxl.load_workbook(file) 
#ws = wb.active
def start(k):
	for i in range(len(k)):
		print(k[i])
		sql = f"""INSERT INTO `id_year`(`id`, `year`) VALUES ('{i}','{k[i]}');"""
		cursor.execute(sql)
		result = cursor.fetchall()
		print(result)
connection = pymysql.connect(host='167.71.38.226',
                             user='test',
                             password='test',
                             db='gamebot',
                             port=3306,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()
def search():
	zap="Forza"
	pidh=[]
	sql = f"""SELECT * FROM `id_name` WHERE 1"""
	cursor.execute(sql)
	result = cursor.fetchall()
	print(result)
	for i in result:
		nume=i['name'].lower()
		if zap.lower() in nume:
			pidh.append(i['id'])
	print(pidh)
def ch(j):
	try:
		int(j)
	except Exception:
		print(".")
#a=[]
#for row in ws.values:
    #main=list(row)
    #a.append(main[2])
#print(a)
#for x in a:
	#print(x)
	#if x is None or x=="Year":
		#a.remove(x)
		#print(a)
#start(a)
search()
connection.commit()

cursor.close()
connection.close()


    	
