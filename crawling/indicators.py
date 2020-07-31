"""
Get technical indicators
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
        for _, row1 in investpy.get_stocks(country=country).iterrows():
            print("-", row1["name"])
            for _, row2 in investpy.technical_indicators(country=country, name=row1["symbol"], product_type="stock", interval="5mins").iterrows():
                query = "INSERT INTO `TechnicalData` (`IndexColumn`, `AddedTime`, `Country`, `Name`, `Symbol`, `Indicator`, `Value`, `Meaning`) VALUES (NULL, CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s);"
                cursor.execute(query, (country, row1["name"], row1["symbol"], row2["technical_indicator"], row2["value"], row2["signal"]))

    connection.close()

    time.sleep(300)
