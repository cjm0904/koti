import pynmea2
import serial, time
import pymysql as sql
conn = sql.connect(host='127.0.0.1', user='root', password='9848', db='koti', charset='utf8')
ser = serial.Serial(port='COM3', baudrate=9600, timeout=1)
global velocity

while True:

    data = ser.readline().decode('utf8')
    # print(data)
    now = round(time.time() * 1000)
    if not data.startswith('$GPGGA'):
        if data.startswith('$GPVTG'):
            data=data.split(',')
            velocity = data[7]
            # print("velocity:", velocity)
        pass
    else:
        data = pynmea2.parse(data)
        if data.lat == '':
            data.lat=0
            data.lat_dir='N'
            data.lon=0
            data.lon_dir='E'
            data.altitude=0
            data.altitude_units=0
            data.num_sats=0
            data.horizontal_dil=0
            velocity = 0
        qry = 'insert into koti(time, latitude, ns_indicator, longtitude, ew_indicator, altitude, units, SatNo, hdop, velocity)'
        qry += 'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        param = (now, data.lat, data.lat_dir, data.lon, data.lon_dir, data.altitude, data.altitude_units, data.num_sats,
                 data.horizontal_dil, velocity)
        print(param)
        try:
            with conn.cursor() as cursor:
                cursor.execute(qry, param)
                conn.commit()

        except TypeError as e:
            print(e)
            continue
