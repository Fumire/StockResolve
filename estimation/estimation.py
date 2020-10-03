import datetime
import time
import typing
import numpy
import sklearn.ensemble
import pandas
import pymysql

while True:
    hour = time.localtime().tm_hour
    if not (10 <= hour <= 16):
        time.sleep(60)
        continue

    with open("/password1.txt", "r") as f:
        connection = pymysql.connect(host="fumire.moe", user="fumiremo_stock", password=f.readline().strip(), db="fumiremo_StockDB", charset="utf8", port=3306)
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    sql = "SELECT `Name`, `Symbol` FROM `NameList` WHERE `Country` LIKE 'south korea' ORDER BY `Name` ASC"
    cursor.execute(sql)

    for name, code in sorted(map(lambda x: (x["Name"], "%06d" % int(x["Symbol"])), cursor.fetchall())):
        sql = "SELECT DISTINCT cast(AddedTime as date) FROM `KRXData` WHERE `Name` LIKE %s ORDER BY cast(AddedTime as date) ASC"
        cursor.execute(sql, (name,))
        result = cursor.fetchall()

        if len(result) == 1:
            continue

        days = sorted(map(lambda x: x["cast(AddedTime as date)"], result))

        whole_data = pandas.DataFrame()
        closed_prices: typing.List[float] = list()

        for day in days:
            sql = "SELECT * FROM `KRXData` WHERE cast(`AddedTime` as date) = %s AND `Name` LIKE %s ORDER BY `AddedTime` ASC"
            cursor.execute(sql, (day, name))
            result = cursor.fetchall()

            prices = numpy.array(list(map(lambda x: x["price"], result)))
            prices = prices / prices[0]

            if len(set(prices)) <= 1:
                continue

            one_data = pandas.DataFrame(data=prices, index=list(map(lambda x: x["AddedTime"].replace(second=0, microsecond=0), result)), columns=[day])
            one_data.loc[datetime.datetime.combine(day, datetime.time(9))] = 1.0
            if one_data.loc[list(filter(lambda x: x.time() >= datetime.time(15, 30), one_data.index))].empty:
                one_data.loc[datetime.datetime.combine(day, datetime.time(15, 30))] = list(one_data.iloc[-1])[0]
            one_data.sort_index(inplace=True)
            one_data = one_data.asfreq(freq="T")
            one_data.drop(labels=list(filter(lambda x: x.time() > datetime.time(15, 30), one_data.index)), axis="index", inplace=True)
            one_data.drop(labels=list(filter(lambda x: x.time() > datetime.datetime.now().time(), one_data.index)), axis="index", inplace=True)
            one_data.interpolate(method="time", inplace=True)
            closed_prices.append(list(one_data.iloc[-1])[0])
            one_data.index = list(map(lambda x: x.time(), one_data.index))

            whole_data = whole_data.join(one_data, how="right")

            if len(closed_prices) > 10:
                break

        if whole_data.shape[0] <= 1:
            continue

        whole_data = whole_data.T

        regressor = sklearn.ensemble.RandomForestRegressor(max_features=None, bootstrap=False, n_jobs=-1, random_state=0)
        regressor.fit(whole_data.iloc[:-1], closed_prices[:-1])

        estimation_value, real_value = regressor.predict(whole_data.iloc[[-1]])[0], closed_prices[-1]

        sql = "SELECT * FROM `Estimations` WHERE `Name` LIKE %s AND `Code` LIKE %s AND `EstimatedDate` = %s"
        cursor.execute(sql, (name, code, days[-1]))

        if cursor.fetchall():
            sql = "UPDATE `Estimations` SET `Estimation` = %s, RealValue = %s WHERE `Name` LIKE %s AND `Code` LIKE %s AND `EstimatedDate` = %s"
            cursor.execute(sql, (str(estimation_value), str(real_value), name, code, days[-1]))
        else:
            sql = "INSERT INTO `Estimations` (`Name`, `Code`, `EstimatedDate`, `Estimation`, `RealValue`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (name, code, days[-1], str(estimation_value), str(real_value)))

        print(name, "Done!!")

    connection.close()
