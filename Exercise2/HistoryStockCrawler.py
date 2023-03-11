import json
import requests
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent

stock_codes = [] #台灣50股票代號
historyPriceInfo=[] #台灣50歷史股價資料 

db_settings = {
    "host": "127.0.0.1",
    "user": "tony",
    "password": "ncu",
    "database": "StockAnaylze",
    "charset": "utf8"
}

def find_Taiwan50():
    # 這邊是用chrome作為範例，可以依照你使用瀏覽器的習慣做修改
    options = chromeOptions()
    options.add_argument("--headless")  # 執行時不顯示瀏覽器
    options.add_argument("--disable-notifications")  # 禁止瀏覽器的彈跳通知
    #options.add_experimental_option("detach", True)  # 爬蟲完不關閉瀏覽器
    chrome = webdriver.Chrome(service=Service('../chromedriver'))
    chrome.get("https://www.cmoney.tw/etf/tw/0050")

    try:
        WebDriverWait(chrome, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[@target='_blank' and @class='stock__link']")))
        stock_elements = chrome.find_elements(By.XPATH, "//a[@target='_blank' and @class='stock__link']")
        for element in stock_elements:
            stock_code = element.get_attribute("href").split('/')[-1]
            stock_codes.append(stock_code)
    except Exception as e:
        raise
    chrome.close()

def findHistoryPriceInfo(url, stock_code):
    user = UserAgent()
    response = requests.get(url, headers = {'User-Agent': user.random})
    dict_json = json.loads(response.text)
    info_list = dict_json.get('data')
    for info in info_list:
        priceInfo = {}
        priceInfo['stock_code'] = stock_code
        priceInfo['date'] = info[0]
        priceInfo['tv'] = info[1]
        priceInfo['t'] = info[2]
        priceInfo['o'] = info[3]
        priceInfo['h'] = info[4]
        priceInfo['l'] = info[5]
        priceInfo['c'] = info[6]
        priceInfo['d'] = info[7]
        priceInfo['v'] = info[8]
        historyPriceInfo.append(priceInfo)

def insertsql():
    try:
        conn = pymssql.connect(**db_settings)
        with conn.cursor() as cursor:
             command ="INSERT INTO [dbo].[historyPriceInfo] (stock_code, date, tv, t, o, h, l, c, d, v) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')"
             print(info)
             print(command % ())
             cursor.execute(command % (info['c'], info['d'], info['t'], float(info['tv'])*1000, 0, info['o'], info['h'], info['i'], float(info['z']), float(info['z_minus_y']), 0))
        conn.commit()
        conn.close()
    except Exception as e:
        raise

def output():
    command ="INSERT INTO [dbo].[historyPriceInfo] (stock_code, date, tv, t, o, h, l, c, d, v) VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\'\n)"
    with open('tmp.txt', 'w') as f:
        for priceInfo in historyPriceInfo:
            f.write(command % (priceInfo['stock_code'], priceInfo['date'], priceInfo['tv'], priceInfo['t'], priceInfo['o'], priceInfo['h'], priceInfo['l'], priceInfo['c'], priceInfo['d'], priceInfo['v']))

find_Taiwan50()
url_format = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=%s&stockNo=%s"
i = 0
for stock_code in stock_codes:
    for year in range(2021, 2024):
        max_month = 12
        if year == 2023:
            max_month = 3
        for month in range(1,max_month+1):
            date = "%d%02d01" % (year, month)
            url = url_format % (date, stock_code)
            findHistoryPriceInfo(url)
            time.sleep(15)
            i+=1
print(i)
output()
#print(datetime.today().strftime('%Y%m%d'))

