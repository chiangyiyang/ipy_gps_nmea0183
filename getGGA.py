import serial
from time import sleep


def checkSum(msg):
  try:
    data = msg[msg.index('$')+1:msg.index('*')]
    cs = 0
    for c in data:
      cs = cs ^ ord(c)
    return cs == int(msg[msg.index('*')+1:], 16)
  except:
    return False


def parseGGA(data):
  try:
    values = data.split(',')
    gga = dict()
    gga['UTC'] = f'{values[1][0:2]}:{values[1][2:4]}:{values[1][4:]}'
    gga['Latitude'] = (float(values[2][0:2]) + (float(values[2][2:])/60)
                       ) * (1 if values[3].upper() == 'N' else -1)
    gga['N/S'] = values[3]
    gga['Longitude'] = (float(values[4][0:3]) + (float(values[4][3:])/60)
                        ) * (1 if values[5].upper() == 'E' else -1)
    gga['E/W'] = values[5]
    gga['Fix'] = ['invalid', 'valid', 'DGPS', 'PPS', 'RTK',
                  'not supported', 'estimated', 'Manual', 'Simulation'][int(values[6])]
    gga['Satellites'] = int(values[7])
    gga['HDOP'] = float(values[8])
    gga['Altitude'] = float(values[9])
    gga['Alt Unit'] = values[10]
    gga['Geoid Separation'] = float(values[11])
    gga['GS Unit'] = values[12]
    gga['Checksum'] = values[14]
    return gga
  except ValueError:
    return None


# port = serial.Serial(port='COM5', baudrate=9600)
print("GPS connected!")
try:
  # while True:
  #   data = port.read_until().decode("ascii")
  #   if ("$GPGGA" in data) and (checkSum(data)):
  #     print(parseGGA(data))
  logs = None
  with open('gps_log.txt', 'r') as f:
    logs = f.readlines()
  for data in logs:
    if ("$GPGGA" in data):
      if(checkSum(data)):
        print(parseGGA(data))
        # sleep(1)
except KeyboardInterrupt:
  # port.close()
  print("GPS disconnected!")
