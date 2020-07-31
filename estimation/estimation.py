import datetime
import time
import numpy
import pandas
import pymysql
import sklearn.ensemble

with open("/password1.txt", "r") as f:
    conn = pymysql.connect(host="fumire.moe", user="fumiremo_stock", password=f.readline().strip(), db="fumiremo_StockDB", charset="utf8", port=3306)
cursor = conn.cursor(pymysql.cursors.DictCursor)

while True:
    sql = "SELECT * FROM `Estimation` WHERE `Complete` = 0 AND `Estimation`.`Algorithm` LIKE 'RandomForest' ORDER BY `Estimation`.`IndexColumn` ASC LIMIT 1"
    cursor.execute(sql)
    row = cursor.fetchone()

    if not row:
        break

    sql = "SELECT * FROM `StockData2` WHERE `code` LIKE '" + str(row["Code"]) + "' ORDER BY `StockData2`.`date` ASC"
    cursor.execute(sql)
    data = pandas.DataFrame(cursor.fetchall())

    macd = data.close.ewm(span=12).mean() - data.close.ewm(span=26).mean()
    macds = macd.ewm(span=9).mean()
    macdo = macd - macds
    data = data.assign(macd=macd, macds=macds, macdo=macdo)
    data.fillna(0, inplace=True)

    ndays_high = data.high.rolling(window=15, min_periods=1).max()
    ndays_low = data.low.rolling(window=15, min_periods=1).min()
    kdj_k = ((data.close - ndays_low) / (ndays_high - ndays_low)) * 100
    kdj_d = kdj_k.ewm(span=5).mean()
    kdj_j = kdj_d.ewm(span=3).mean()
    data = data.assign(kdj_k=kdj_k, kdj_d=kdj_d, kdj_j=kdj_j)
    data.fillna(0, inplace=True)
    data.replace(numpy.inf, 0, inplace=True)

    x_train, y_train, date = data.drop(columns=["IndexColumn", "name", "code", "date", "close"]), data["close"].tolist(), data["date"].tolist()

    regr = sklearn.ensemble.RandomForestRegressor(random_state=0, n_jobs=1)
    regr.fit(x_train[:-row["Days"]], y_train[row["Days"]:])

    y_pred = regr.predict(x_train)

    error_rate = numpy.mean([(abs(a - b) / a if a else 1) for a, b in zip(y_train[row["Days"]:], y_pred[:-row["Days"]])]) * 100
    gain_rate = ((y_pred[-1] - y_train[-1]) / y_train[-1] * 100) if y_train[-1] else 0

    for d, r, p in list(zip(date[:-row["Days"]], y_train[row["Days"]:], y_pred[:-row["Days"]]))[-400:]:
        sql = "INSERT INTO `EstimatedValues` (`IndexColumn`, `Algorithm`, `Identification`, `Date`, `RealValue`, `PredictValue`) VALUES (NULL, 'RandomForest', '%s', '%s', '%d', '%f');" % (row["Identification"], str(d), r, p)
        cursor.execute(sql)

    for i, p in enumerate(y_pred[-row["Days"]:]):
        sql = "INSERT INTO `EstimatedValues` (`IndexColumn`, `Algorithm`, `Identification`, `Date`, `RealValue`, `PredictValue`) VALUES (NULL, 'RandomForest', '%s', '%s', NULL, '%f');" % (row["Identification"], str(d + datetime.timedelta(days=i + 1)), p)
        cursor.execute(sql)

    sql = "UPDATE `Estimation` SET `ErrorRate` = '%f', `GainRate` = '%f', `Complete` = '1' WHERE `Identification` = '%s'" % (error_rate, gain_rate, row["Identification"])
    cursor.execute(sql)

    print(row["Identification"], "Done!!", error_rate, gain_rate)

while True:
    sql = "SELECT * FROM `Estimation` WHERE `Complete` = 0 AND `Estimation`.`Algorithm` LIKE 'AdaBoost' ORDER BY `Estimation`.`IndexColumn` ASC LIMIT 1"
    cursor.execute(sql)
    row = cursor.fetchone()

    if not row:
        break

    sql = "SELECT * FROM `StockData2` WHERE `code` LIKE '" + str(row["Code"]) + "' ORDER BY `StockData2`.`date` ASC"
    cursor.execute(sql)
    data = pandas.DataFrame(cursor.fetchall())

    macd = data.close.ewm(span=12).mean() - data.close.ewm(span=26).mean()
    macds = macd.ewm(span=9).mean()
    macdo = macd - macds
    data = data.assign(macd=macd, macds=macds, macdo=macdo)
    data.fillna(0, inplace=True)

    ndays_high = data.high.rolling(window=15, min_periods=1).max()
    ndays_low = data.low.rolling(window=15, min_periods=1).min()
    kdj_k = ((data.close - ndays_low) / (ndays_high - ndays_low)) * 100
    kdj_d = kdj_k.ewm(span=5).mean()
    kdj_j = kdj_d.ewm(span=3).mean()
    data = data.assign(kdj_k=kdj_k, kdj_d=kdj_d, kdj_j=kdj_j)
    data.fillna(0, inplace=True)
    data.replace(numpy.inf, 0, inplace=True)

    x_train, y_train, date = data.drop(columns=["IndexColumn", "name", "code", "date", "close"]), data["close"].tolist(), data["date"].tolist()

    regr = sklearn.ensemble.AdaBoostRegressor(random_state=0)
    regr.fit(x_train[:-row["Days"]], y_train[row["Days"]:])

    y_pred = regr.predict(x_train)

    error_rate = numpy.mean([(abs(a - b) / a if a else 1) for a, b in zip(y_train[row["Days"]:], y_pred[:-row["Days"]])]) * 100
    gain_rate = ((y_pred[-1] - y_train[-1]) / y_train[-1] * 100) if y_train[-1] else 0

    sql = "UPDATE `Estimation` SET `ErrorRate` = '%f', `GainRate` = '%f', `Complete` = '1' WHERE `Identification` = '%s'" % (error_rate, gain_rate, row["Identification"])
    cursor.execute(sql)

    print(row["Identification"], "Done!!", error_rate, gain_rate)

conn.close()

time.sleep(60)
