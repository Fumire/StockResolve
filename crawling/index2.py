"""
index2.py: get current index data
"""
import time
import pandas
import pymysql
import requests

while True:
    for site in ["https://www.investing.com/indices/japan-indices", "https://www.investing.com/indices/south-korea-indices", "https://www.investing.com/indices/usa-indices"]:
        response = requests.get(site)

        data = pandas.read_html(response.text)[0]

        data = data[["Symbol", "Last"]]
        data.dropna(inplace=True)

        print(data)

        with open("/password1.txt", "r") as f:
            connection = pymysql.connect(host="fumire.moe", user="fumiremo_stock", password=f.readline().strip(), db="fumiremo_StockDB", charset="utf8", port=3306)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        for index, row in data.iterrows():
            sql = "INSERT INTO `IndexData2` (`Symbol`, `Value`) VALUES (%s, %s)"
            cursor.execute(sql, (row["Symbol"], row["Last"]))

        connection.close()

    time.sleep(300)
