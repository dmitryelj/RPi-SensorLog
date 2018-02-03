# RPi-SensorLog
Raspberry Pi tool for saving and collecting data from different sensors (MPU-9250, etc)

# Features

- Different sensors support (this version support MPU9250 (accel, gyro, mag) and BMP280 (baro))

- Split logs to day patterns (YYYY-mm-dd)

- Web-server for data access

# Screenshots

![View](/Screenshots/scr01.png)

# Usage

1) Install

git clone https://github.com/dmitryelj/RPi-SensorLog.git

2) Run

python Python/sensorLog.py --delay_ms=100 --data="gyro|mag"

python Python/sensorLog.py --delay_ms=500 --data="all"

3) Data access: http://192.168.0.110:8000 (see IP address when program start)

4) Autostart: add app run to /etc/rc.local (see Raspberry Pi manual)
