# RPi-SensorLog
Raspberry Pi tool for saving and collecting data from different sensors (MPU-9250, etc)

# Features

- Different sensors support (this version support MPU9250 (accel, gyro, mag) and BMP280 (baro))

- Split log files to day patterns (YYYY-mm-dd)

- Web-server for data access

SensorLog saves data to a CSV file, like this:

0,2018-01-26 21:17:40.571598,88,108,7770,30208,20224,23296

1,2018-01-26 21:17:41.484293,166,130,7760,30208,19968,23808

2,2018-01-26 21:17:42.019811,118,86,7756,29952,20736,23296

3,2018-01-26 21:17:42.555163,120,88,7792,29696,20224,23296

4,2018-01-26 21:17:43.090846,126,98,7770,29952,20736,23552

5,2018-01-26 21:17:43.626676,126,100,7838,30208,19968,24064

It can be visualized by any free online tool, like https://plot.ly/create/.

# Screenshots

![View](/Screenshots/scr01.png)

# Usage

Install:

git clone https://github.com/dmitryelj/RPi-SensorLog.git

Run:

python Python/sensorLog.py --delay_ms=100 --data="gyro|mag"

python Python/sensorLog.py --delay_ms=500 --data="all"

Data access: 

http://192.168.0.110:8000 (see IP address when program start)


Autostart: 

add app run to /etc/rc.local (see Raspberry Pi manual)
