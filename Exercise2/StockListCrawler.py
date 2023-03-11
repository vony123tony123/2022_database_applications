import pymssql
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service

db_settings = {
    "host": "127.0.0.1",
    "user": "tony",
    "password": "ncu",
    "database": "StockAnaylze",
    "charset": "utf8"
}

# 儲存台灣50前10的陣列
taiwan50 = []

# 搜尋台灣50前10
def find_Taiwan50():
    # 這邊是用chrome作為範例，可以依照你使用瀏覽器的習慣做修改
    options = chromeOptions()
    options.add_argument("--headless")  # 執行時不顯示瀏覽器
    options.add_argument("--disable-notifications")  # 禁止瀏覽器的彈跳通知
    #options.add_experimental_option("detach", True)  # 爬蟲完不關閉瀏覽器
    chrome = webdriver.Chrome(service=Service('./chromedriver'))

    chrome.get("https://www.cmoney.tw/etf/tw/0050")

    # 練習2
    try:
        WebDriverWait(chrome, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[@target='_blank' and @class='stock__link']")))
        stock_elements = chrome.find_elements(By.XPATH, "//a[@target='_blank' and @class='stock__link']")
        for element in stock_elements:
            taiwan50.append(element.text)
    except Exception as e:
        print(e)
    chrome.close()

# 載入SQL (若為台灣50前10，isTaiwan50 = 1)
def find_stock(url, start, end):
    try:
        conn = pymssql.connect(**db_settings)
        # 練習2
        with conn.cursor() as cursor:
            command ="INSERT INTO [dbo].[stockInfo] (stock_code, name, type, category, isTaiwan50) VALUES (%s, %s, %s, %s, %d)"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            if url[-1] == '4':
                result = soup.select("tr td b")[4]
            elif url[-1] == '2':
                result = soup.select("tr td b")[0]
            print(result)
            while True:
                result = result.find_next("tr")
                info = result.find_all("td")
                if info[0].text.strip() == end:
                    break
                stock_code = "\'"+info[0].text.split()[0]+"\'"
                name = "\'" +info[0].text.split()[1]+"\'"
                market_type = "\'"+info[3].text+"\'"
                category = "\'"+info[4].text+"\'"
                isTaiwan50 = 0
                if info[0].text.split()[1] in taiwan50:
                    isTaiwan50 = 1
                print(command % (stock_code, name, market_type, category, isTaiwan50))
                cursor.execute(command % (stock_code, name, market_type, category, isTaiwan50))
        conn.commit()
        conn.close
    except Exception as e:
       print(e)

find_Taiwan50()
find_stock("https://isin.twse.com.tw/isin/C_public.jsp?strMode=4", "股票", "特別股")
find_stock("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2", "股票", "上市認購(售)權證")