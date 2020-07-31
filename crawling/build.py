"""
build.py: Build stock data
"""
import datetime
import time
import investpy
import pymysql

with open("/password1.txt", "r") as f:
    connection = pymysql.connect(host="fumire.moe", user="fumiremo_stock", password=f.readline().strip(), db="fumiremo_StockDB", charset="utf8", port=3306)
cursor = connection.cursor(pymysql.cursors.DictCursor)

for country in ["south korea", "japan", "united states"]:
    print(country)
    for _, row1 in investpy.get_stocks(country=country).iterrows():
        print("-", row1["name"])
        time.sleep(1)
        for date, row2 in investpy.get_stock_historical_data(stock=row1["symbol"], country=country, from_date="01/01/1900", to_date=datetime.datetime.today().strftime("%d/%m/%Y"), order="descending").iterrows():
            query = "SELECT * FROM `StockData` WHERE `country` LIKE '%s' AND `Name` LIKE '%s' AND `Symbol` LIKE '%s' AND `Date` = '%s'" % (country, row1["name"], row1["symbol"], date.date())
            cursor.execute(query)

            if cursor.fetchall():
                break

            query = "INSERT INTO `StockData` (`IndexColumn`, `Country`, `Name`, `Symbol`, `Date`, `Open`, `High`, `Low`, `Close`, `Volume`, `Currency`) VALUES (NULL, '%s', '%s', '%s', '%s', '%f', '%f', '%f', '%f', '%d', '%s');" % (country, row1["name"], row1["symbol"], date.date(), row2["Open"], row2["High"], row2["Low"], row2["Close"], row2["Volume"], row2["Currency"])
            cursor.execute(query)

            print("--", date.date())

        time.sleep(1)

connection.close()
