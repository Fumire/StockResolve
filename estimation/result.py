import time
import pymysql

while True:
    hour = time.localtime().tm_hour
    if not (10 <= hour <= 16):
        time.sleep(60)
        continue

    with open("/password1.txt", "r") as f:
        connection = pymysql.connect(host="fumire.moe", user="fumiremo_stock", password=f.readline().strip(), db="fumiremo_StockDB", charset="utf8", port=3306)
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    sql = "SELECT `Name` FROM `Estimations` WHERE `EstimatedDate` = CURRENT_DATE ORDER BY `Name` ASC"
    cursor.execute(sql)

    for name in sorted(map(lambda x: x["Name"], cursor.fetchall())):
        try:
            sql = "SELECT `price` FROM `KRXData` WHERE `Name` LIKE %s AND cast(`AddedTime` as date) = CURRENT_DATE ORDER BY `AddedTime` ASC LIMIT 1"
            cursor.execute(sql, (name,))
            start = cursor.fetchone()["price"]

            sql = "SELECT `price` FROM `KRXData` WHERE `Name` LIKE %s AND cast(`AddedTime` as date) = CURRENT_DATE ORDER BY `AddedTime` DESC LIMIT 1"
            cursor.execute(sql, (name,))
            end = cursor.fetchone()["price"]

            sql = "UPDATE `Estimations` SET `RealValue` = %s WHERE `Name` LIKE %s AND `EstimatedDate` = CURRENT_DATE"
            cursor.execute(sql, (str(end / start), name))

            print(name, "Done!!")
        except TypeError:
            continue

    connection.close()
