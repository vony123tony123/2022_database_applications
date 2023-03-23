import mplfinance as mpf
import pymssql
import json
import pandas as pd
import numpy as np

db_settings = {
    "host": "127.0.0.1",
    "user": "tony",
    "password": "ncu",
    "database": "StockAnaylze",
    "charset": "utf8"
}

# 取DB裡的歷史資料
def getSqlData(stock_code):
    result = []
    try:  
        conn = pymssql.connect(**db_settings)
        with conn.cursor() as cursor:
            command = "SELECT date, o, h, l, c, v FROM historyPriceInfo WHERE date like '2021-12-%' and stock_code = stock_code;"
            cursor.execute(command)
            result = cursor.fetchall()
    except Exception as ex:
        print(ex)
    conn.close()
    return result

if __name__ == '__main__':
    sqlDatas = getSqlData(2023)
    result = []
    for sqlData in sqlDatas:
        sqlData = list(sqlData)
        sqlData[0] = sqlData[0];
        sqlData[1] = float(sqlData[1])
        sqlData[2] = float(sqlData[2])
        sqlData[3] = float(sqlData[3])
        sqlData[4] = float(sqlData[4])
        sqlData[5] = float(sqlData[5])
        result.append(sqlData)
        
    arr_df = pd.DataFrame(result)
    arr_df.index = pd.to_datetime(arr_df[0])
    arr_df = arr_df.drop(columns=[0])
    arr_df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    arr_df.index.name = "Date"
    print(arr_df)

    mc = mpf.make_marketcolors(up='r',
                           down='g',
                           edge='',
                           wick='inherit',
                           volume='inherit')
    s = mpf.make_mpf_style(base_mpf_style='charles', marketcolors=mc)

    mpf.plot(arr_df, type='candle', style=s)