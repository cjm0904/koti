import pynmea2
import serial, time
import pymysql as sql

conn = sql.connect(host='127.0.0.1', user='root', password='ziumks',db='koti', charset='utf8')
ser = serial.Serial(port='COM8', baudrate=9600, timeout=1)

while True:
    data = ser.readline().decode('utf8')
    now = round(time.time() * 1000)
    if not data.startswith('$GPGGA'):
        pass
    else:
        data = pynmea2.parse(data)
        qry = 'insert into koti(time, latitude, ns_indicator, longtitude, ew_indicator, altitude, units, SatNo, hdop)'
        qry+= 'values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        param = (now, data.lat, data.lat_dir, data.lon, data.lon_dir, data.altitude, data.altitude_units, data.num_sats, data.horizontal_dil)
        print(param)
        try:
            with conn.cursor() as cursor:
                cursor.execute(qry, param)
                conn.commit()
            
        except TypeError as e:
            print(e)
