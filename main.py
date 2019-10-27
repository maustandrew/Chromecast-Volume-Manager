import pychromecast
import sys
import time

castName = ""
chromecast = ""

def reconnect():
    time.sleep(60)
    print("Attempting to reconnect")

def getDevice():
    #Attempts to find device with friendly name
    global castName
    cc = ''
    chromecasts = pychromecast.get_chromecasts()
    for x in chromecasts:
        if x.device.friendly_name == castName:
            cc = x
            break
    if cc == '':
        return "Error no chromecast found with that name"
    else:
        return cc

def init():
    #Sets up device info and send Initial Attempt to connect to the device
    global castName
    global chromecast
    castName = sys.argv[1]
    print("Managing the volume of " + castName)
    chromecast = getDevice()
    print(chromecast)
    if chromecast.startswith("Chromecast") == True:
        try:
            chromecast.wait()
        except:
            print("Cant connect to Chromecast")
            reconnect()
    else:
        print(chromecast)
        reconnect()

init()
