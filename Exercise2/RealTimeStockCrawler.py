import requests
import json
from fake_useragent import UserAgent
import pymssql
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
import os

db_settings = {
    "host": "127.0.0.1",
    "user": "tony",
    "password": "ncu",
    "database": "StockAnaylze",
    "charset": "utf8"
}

def find_StockInfo(url):
	user = UserAgent()
	response = requests.get(url, headers = {'User-Agent': user.random})
	dict_json = json.loads(response.text)
	info = dict_json['msgArray'][0]
	if info['tv'] == "-":
		info['tv'] = 0
	if info['z'] == "-":
		info['z'] = 0
		info['z_minus_y'] = 0
	else:
		info['z_minus_y'] = float(info['z']) - float(info['y'])
	return info

def insertsql(info):
	try:
		conn = pymssql.connect(**db_settings)
		with conn.cursor() as cursor:
			 command ="INSERT INTO [dbo].[priceInfo] (stock_code, date, time, tv, t, o, h, l, c, d, v) VALUES (\'%s\', \'%s\', \'%s\', %d, %d, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', %d)"
			 print(info)
			 print(command % (info['c'], info['d'], info['t'], float(info['tv'])*1000, 0, info['o'], info['h'], info['i'], float(info['z']), float(info['z_minus_y']), 0))
			 cursor.execute(command % (info['c'], info['d'], info['t'], float(info['tv'])*1000, 0, info['o'], info['h'], info['i'], float(info['z']), float(info['z_minus_y']), 0))
		conn.commit()
		conn.close()
	except Exception as e:
		raise

def find_realTimeStockInfo():
	stock_info = find_StockInfo("https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_2330.tw&json=1&delay=0")
	insertsql(stock_info)
	stock_info = find_StockInfo("https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_2317.tw&json=1&delay=0")
	insertsql(stock_info)
	return

try:
	scheduler = BlockingScheduler()
	now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	end = datetime.today() + timedelta(minutes=15)
	end = end.strftime('%Y-%m-%d %H:%M:%S')
	scheduler.add_job(find_realTimeStockInfo, 'interval', minutes=5, start_date=now, end_date=end, next_run_time=now)
	scheduler.start()
except Exception as e:
	os._exit()
	raise


