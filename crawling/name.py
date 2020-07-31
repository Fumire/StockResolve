"""
Get stock name data
"""
import time
import investpy
import pymysql

while True:
    with open("/password1.txt", "r") as f:
        connection = pymysql.connect(host="fumire.moe", user="fumiremo_stock", password=f.readline().strip(), db="fumiremo_StockDB", charset="utf8", port=3306)
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    query = "TRUNCATE `NameList`"
    cursor.execute(query)

    for country in ["south korea", "japan", "united states"]:
        print(country)
        for _, row in investpy.get_stocks(country=country).iterrows():
            print("-", row["name"])
            query = "INSERT INTO `NameList` (`IndexColumn`, `Country`, `Name`, `Symbol`) VALUES (NULL, %s, %s, %s);"
            cursor.execute(query, (country, row["name"], row["symbol"]))

    connection.close()

    time.sleep(86400)
