from influxdb import InfluxDBClient
from datetime import datetime
from datetime import timedelta
import numpy
import pylab
import array
import matplotlib

client = InfluxDBClient(host="localhost", port=8086, database='mmp')

time = input("Date et heure du debut de l'analyse : exemple 2018-08-27 06:56:10 ")
time = time + '.000000'
time2 = None
timeBeforeChange = None



def addTime(time):
    TimeConverted = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    Time2Converted = TimeConverted + timedelta(minutes=2)
    time2 = Time2Converted.strftime("%Y-%m-%d %H:%M:%S.%f")
    return time2


queryResult = []
k = 0
while k < 8:
    time2 = addTime(time)
    rs = client.query("SELECT * FROM mmp_metrics where time > '" + time + "' AND time < '" + time2 + "'")
    queryResult.insert(k, list(rs.get_points(measurement='mmp_metrics')))
    time = time2
    k += 1

def moyenne(sum, length):
  return sum / length

def function(queryResult):
    wattArr = []
    iterations = []
    delete = []
    moyWatt = []
    sum = 0
    i = 0
    json_body = []
    while i < len(queryResult):
        wattArr.insert(i, queryResult[i]['awatt'])
        iterations.insert(i, i)
        sum = sum + queryResult[i]['awatt']

        result = moyenne(sum, len(wattArr))
        moyWatt.insert(len(moyWatt), result)

        if (queryResult[i]["awatt"] > (result + (result * 0.4 / 100)) or queryResult[i]["awatt"] < (result - (result * 0.4 / 100))):
                if(queryResult[i]["awatt"] < (result + (result * 1 / 100)) or queryResult[i]["awatt"] > (result - (result * 1 / 100))):
                    print (queryResult[i]["awatt"])

                    json_body.append({
                        "measurement": 'data',
                        "time": queryResult[i]["time"],
                        "fields": {
                            "awatt":queryResult[i]["awatt"]
                        }
                    })
        i += 1

    print(json_body)
    client.write_points(json_body)

    pylab.figure()
    pylab.plot(iterations, wattArr)
    pylab.plot(iterations, moyWatt)
    pylab.pause(0.05)
pylab.show(block=True)

j = 0
while j < 8:
    function(queryResult[j])
    j += 1

input("Appuyer sur une touche pour quitter...")
