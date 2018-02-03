# Sensor data logging tool for Raspberry Pi
# dmitryelj@gmail.com
#
# This version support MPU9250 (accel, gyro, mag) and BMP280 (baro)

import math
import datetime, time
import sys, os, threading, socket
import argparse
import SimpleHTTPServer
import SocketServer

is_raspberry = os.name != "nt" and os.uname()[0] == "Linux"

# Sensor select
sensor1 = None
sensor2 = None
if is_raspberry:
    from mpu9250 import mpu9250
    sensor1 = mpu9250()

# Web server to access data
PORT_NUMBER = 8000
httpd = None

def readData():
    if is_raspberry:
        # 3x accelerometer, 3x gyro, 3x magnetometer, 1x temperature
        #data = sensor.read_all()
        tempOut, ax,ay,az, gx,gy,gz, mx,my,mz = sensor1.read_all()
        # Grab the X, Y, Z components from the reading and print them out.
        return ax,ay,az, gx,gy,gz, mx,my,mz
    else:
        # Simulation only, for testing
        return 0,0,0, 1,1,1, 2,2,2

def getIPAddress():
    try:
        if os.name == "nt":
          hostname = socket.gethostname()
          return socket.gethostbyname(hostname)
        else:
          s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
          s.connect(("8.8.8.8", 80))
          return s.getsockname()[0]
    except:
        return "-"

if __name__ == "__main__":
    print "Sensor data logging tool for Raspberry Pi v0.1b"
    print "Run:\npython sensorLog.py [--delay_ms=100] [--data=accel|gyro|mag|baro]"
    print ""

    # Recording parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("--delay_ms", dest="delay_ms", default="500")
    parser.add_argument("--data", dest="data", default="all")
    args = parser.parse_args()
    delay_ms = int(args.delay_ms)
    data_type = args.data

    # HTTP server to access log files
    def httpServerFunc():
        global httpd
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()

    print "Http server starting. Use http://{}:{} to access your logs.\n".format(getIPAddress(), PORT_NUMBER)
    HTTPHandler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT_NUMBER), HTTPHandler)
    serverThread = threading.Thread(target=httpServerFunc)
    serverThread.start()

    # Log files pattern
    def getFileName(dt):
        return dt.strftime('%Y-%m-%d.txt')

    index = 0
    # Get last index from log file
    try:
        fh = open(getFileName(), "r")
        data = fh.readlines()
        if len(data) > 0:
            last = data[-1]
            # 12,2018-01-26 16:26:34,0,0,0 => 12
            index_last = last.split(",")[0]
            index = int(index_last) + 10
    except Exception, e:
        pass # print "Cannot read last index: %s" % str(e)
    # print "Last index found: %d" % index

    # Start logging
    try:
        str_buf = ""
        print "Sensor data:"
        while True:
            now = datetime.datetime.now()
            timestamp = now.strftime('%Y-%m-%d %H:%M:%S.%f')
            if now.hour == 0 and now.minute == 0 and now.second == 0:
                # Save previous buffer for last day
                if len(str_buf) > 0:
                    with open(getFileName(now - datetime.timedelta(seconds=5)), "a") as myfile:
                        myfile.write(str_buf)
                        str_buf = ""

                # new day started, reset index
                index = 0
        
            accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z = readData()
            str_data = "{},{}".format(index, timestamp)
            if "accel" in data_type or "all" in data_type:
                str_data += ",{},{},{}".format(accel_x, accel_y, accel_z)
            if "gyro" in data_type or "all" in data_type:
                str_data += ",{},{},{}".format(gyro_x, gyro_y, gyro_z)
            if "mag" in data_type or "all" in data_type:
                str_data += ",{},{},{}".format(mag_x, mag_y, mag_z)
            print str_data
        
            # Add to buffer (write with blocks to save memory card life)
            str_buf += str_data + '\n'
            if index > 0 and index % 100 == 0:
                # Save log
                filename = getFileName(now)
                with open(filename, "a") as myfile:
                    myfile.write(str_buf)
                    str_buf = ""
                    print "%s saved" % filename

            index += 1
            time.sleep(delay_ms*0.001)

    except KeyboardInterrupt:
        pass

    httpd.shutdown()

    print "Done"

