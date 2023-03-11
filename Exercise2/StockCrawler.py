import calendar
import pymssql
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service

# 根據自己的Database來填入資訊
db_settings = {
    "host": "127.0.0.1",
    "user": "tony",
    "password": "ncu",
    "database": "StockAnaylze",
    "charset": "utf8"
}

#特殊節日
holiday_dir = {}

# 爬蟲
def crawler():

    # 這邊是用chrome作為範例，可以依照你使用瀏覽器的習慣做修改
    options = chromeOptions()
    options.add_argument("--headless")  # 執行時不顯示瀏覽器
    options.add_argument("--disable-notifications")  # 禁止瀏覽器的彈跳通知
    #options.add_experimental_option("detach", True)  # 爬蟲完不關閉瀏覽器
    chrome = webdriver.Chrome(service=Service('../chromedriver'))

    chrome.get("https://www.wantgoo.com/global/holiday/twse")
    try:
        # 等元件跑完再接下來的動作，避免讀取不到內容
        WebDriverWait(chrome, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//tbody[@id='holidays']//tr//th")))
        # 練習1
        holiday_list = chrome.find_elements(By.XPATH,"//tbody[@id = 'holidays']//tr")
        for holiday in holiday_list:
            WebDriverWait(holiday, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "td")))
            WebDriverWait(holiday, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "th")))
            holiday_arr = holiday.text.split(' ')
            date = holiday_arr[0].replace('/','-')
            name = holiday_arr[2]
            holiday_dir[date] = name
    except TimeoutException as e:
        print(e)    
    #chrome.close()


# 載入SQL
def insertSQL():
    # 非休市日
    work_count = 0
    year = 2023
    try:
        conn = pymssql.connect(**db_settings)
        # 請根據自己的資料表修改command
        command = "INSERT INTO [dbo].[calendar] (date, day_of_stock, other) VALUES (%s, %d, %s)"
        # 練習1
        cursor = conn.cursor()
        with conn.cursor() as cursor:
            for month in range(1,13):
                for day in range(1, calendar.monthrange(year, month)[1]+1):
                    date = f"{year}-{month:02d}-{day:02d}"
                    weekday = calendar.weekday(year, month, day)
                    if date in holiday_dir:
                        print(holiday_dir[date])
                        cursor.execute(command % ("\'"+date+"\'", -1, "\'"+holiday_dir[date]+"\'"))
                    elif weekday == 5 or weekday == 6:
                        cursor.execute(command % ("\'"+date+"\'", -1, "NULL"))
                    else:
                        work_count+=1
                        cursor.execute(command % ("\'"+date+"\'", work_count, "NULL"))
            conn.commit()
        
    except Exception as e:
        print(e)
    conn.close()

crawler()
insertSQL()