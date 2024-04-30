import datetime
from datetime import timedelta
import time
import pandas as pd
import requests
from math import ceil
def get_data():
    headers = {
    "authority": "stock.xueqiu.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "origin": "https://xueqiu.com",
    "referer": "https://xueqiu.com/",
    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
    url = "https://stock.xueqiu.com/v5/stock/realtime/quotec.json"
    params = {
        # 'symbol': 'SH601127,SZ002786,SH600733,SZ002238,SZ002712,SH600520,SH601985',
        'symbol': 'SZ002786,SH600520',
        '_':str(int(time.time() * 1000))
    }
    response = requests.get(url, headers=headers, params=params)
    # print(response.json())
    names = {
        # 'SH601127':'赛宝',
        'SZ002786':{'name':'银宝山新','hand':0},
        # 'SH600733':{'name':'北汽','hand':2200}, 
        # 'SZ002325':'洪宝'
        # 'SZ002238':'威宝',
        # 'SZ002712':'思宝',
        'SH600520':{'name':'文一科技','hand':0},
        # 'SH601985':'核宝',
        # 'SZ000056':'皇宝',
        # 'SZ000938':'紫光',
        # 'SH603960':'克来',
        # 'SH600678':'金顶',
        # 'SH600400':{'name':'红豆','hand':3500},
        # 'SZ000628':{'name':'高新','hand':300}
        }
    data = response.json().get('data')
    end_data = []
    print('*'*50)
    if data:
        for da in data:
            # symbol = {names[da['symbol']]:[
            #           {'当前':da['current']},
            #           {'涨幅':da['percent']},
            #         #   {'价变':da['chg']},
            #         #   {'最高':da['high']},
            #         #   {'最低':da['low']},
            #         #   {'开盘':da['open']},
            #         #   {'昨价':da['last_close']}
            #         ]}
            # print(symbol)
            # end_data.append(symbol)
            
            percent = da['percent']
            # chg = (da['chg']-0.1131) * 1600
            chg = da['chg']
            # print(chg) 
            # chg2 = (da['chg'] - 0.02) * 7000
            # chg = chg2 + chg1
            
            if percent <=0:
                print(f'\033[94m{(datetime.datetime.now()+timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")}\033[0m {names[da["symbol"]]["name"]}:{da["current"]} 今日\033[92m负债:{chg * names[da["symbol"]]["hand"]},涨跌幅:{percent}\033[0m')
            else:
                print(f'\033[94m{(datetime.datetime.now()+timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")}\033[0m {names[da["symbol"]]["name"]}:{da["current"]} 今日\033[91m盈利:{chg * names[da["symbol"]]["hand"]},涨跌幅:{percent}\033[0m')
            # if percent <=0:
            #     print(f'\033[94m{(datetime.datetime.now()+timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")}\033[0m,{names[da["symbol"]]}:{da["current"]},{da["chg"]},\033[92m{percent},{ceil(chg)}\033[0m')
            # else:
            #     print(f'\033[94m{(datetime.datetime.now()+timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")}\033[0m,{names[da["symbol"]]}:{da["current"]},{da["chg"]},\033[91m{percent},{ceil(chg)}\033[0m')
    # print(end_data)
    # stock_data = [(key, *list(map(lambda x: list(x.values())[0], value))) for d in end_data for key, value in d.items()]
    # df = pd.DataFrame(stock_data, columns=['股票名称', '当前', '涨幅', '价变', '最高', '最低', '开盘', '昨价'])
    # df = pd.DataFrame(stock_data)
    # df = pd.DataFrame(stock_data, columns=['name', 'now', 'perc', 'chg', 'high', 'low', 'open', 'y'])
    # df = pd.DataFrame(stock_data, columns=['name', 'now', 'perc'])
    # print(df)
    # print(end_data)
    return 


if __name__ == "__main__":
    while True:
        get_data()
        time.sleep(0.75)
        