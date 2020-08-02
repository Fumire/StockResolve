"""
KRX.py: get KRX data
"""
import fake_useragent
import requests
import pandas
import pymysql

columns = sorted(["quant", "ask_buy", "amount", "market_sum", "operating_profit", "per", "open_val", "ask_sell", "prev_quant", "property_total", "operating_profit_increasing_rate", "roe", "high_val", "buy_total", "frgn_rate", "debt_total", "net_income", "roa", "low_val", "sell_total", "listed_stock_cnt", "sales", "eps", "pbr", "sales_increasing_rate", "dividend", "reserve_ratio"])

user_agent = fake_useragent.UserAgent()
session = requests.Session()

while True:
    whole_data = dict()

    for i in range(2):
        for column in columns:
            print(column)

            request_url = "https://finance.naver.com/sise/field_submit.nhn?menu=market_sum&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.nhn%3Fsosok%3D" + str(i) + "&fieldIds=" + column
            session.headers.update({"User-Agent": user_agent.random})
            session.post(request_url)

            page = 0
            while True:
                page += 1
                print("-", page)

                raw_data = session.post("https://finance.naver.com/sise/sise_market_sum.nhn?&page=" + str(page))
                data = pandas.read_html(raw_data.text)[1]

                data.dropna(axis="columns", how="all", inplace=True)
                data.dropna(axis="index", how="any", inplace=True)

                data.rename(columns={"종목명": "name", "현재가": "price"}, inplace=True)

                if data.empty:
                    break

                for index, row in data.iterrows():
                    if row["name"] not in whole_data:
                        whole_data[row["name"]] = dict()
                        whole_data[row["name"]]["price"] = row["price"]
                    whole_data[row["name"]][column] = row[data.columns[-1]]

    with open("/password1.txt", "r") as f:
        connection = pymysql.connect(host="fumire.moe", user="fumiremo_stock", password=f.readline().strip(), db="fumiremo_StockDB", charset="utf8", port=3306)
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    for name in whole_data:
        sql = "INSERT INTO `KRXData` (`Name`,`" + "`,`".join(whole_data[name].keys()) + "`) VALUES ('" + name + "'," + ",".join(list(map(lambda x: "'" + str(x) + "'", whole_data[name].values()))) + ")"
        cursor.execute(sql)

    connection.close()
