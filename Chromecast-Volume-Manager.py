import pychromecast
import sys
import time

castName = ""
chromecast = ""
volume = 20

def reconnect(code):
    global chromecast
    """
    Code System:
    Code 0: Chromecast found but failed to connect; Error in init()
    Code 1: Chromecast failed to be located; Error in getDevice()
    Code 2: Chromecast disconnected, turned off, or updating; Error in maintain() or changeVolume()
    """ 
    if code == 0:
        print('Attempting to reconnect in 30 seconds...')
        time.sleep(30)
        try:
            chromecast.wait()
            print("Connected")
            maintain()
        except:
            reconnect(0)
    elif code == 1:
        print('Attempting to reconnect in 30 seconds...')
        time.sleep(30)
        chromecast = getDevice()
        if type(chromecast) == pychromecast.Chromecast:
            try:
                chromecast.wait()
                print("Successfully connected to Chromecast")
                maintain()
            except:
                print("Failed to connect to Chromecast")
                reconnect(1)
        else:
            print(chromecast)
            reconnect(0)
    elif code == 3:
        print('Attempting to reconnect in 30 seconds...')
        time.sleep(30)
        try:
            chromecast.wait()
            print("Connected")
            maintain()
        except:
            reconnect(0)

def changeVolume():
    global chromecast
    global volume
    try:
        if chromecast.status.volume_level < 1:
            print('[STATUS] %s is currently at %d%%' % (castName, round(chromecast.status.volume_level * 100)))
            time.sleep(120)
            maintain()
        elif chromecast.status.volume_level == 1:
            chromecast.volume_down(1 - volume/100)
            time.sleep(2)
            print('[STATUS] %s is changed to %d%% from 100%%' % (castName, round(chromecast.status.volume_level * 100)))
            time.sleep(120)
            maintain()
    except:
        reconnect(2)

def maintain():
    global chromecast
    global castName
    try:
        while chromecast.status.status_text != "":
            print('[STATUS] %s is currently casting' % castName)
            time.sleep(300)
        else:
            changeVolume()
    except:
        reconnect(2)

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
    global volume
    try:
        castName = sys.argv[1]
    except:
        castName = input("[ERROR] No Chromecast name given, please input the name of a Chromecast on your local network: ")
    try:
        volume = int(sys.argv[2])
        print(volume)
    except:
        print("No volume was passed into the command line, Chromecast Volume Manager will set your Chromecast to a default volume of %s" % volume)
    print("Managing the volume of " + castName)
    print("Volume set to %s" % volume)
    chromecast = getDevice()
    if type(chromecast) == pychromecast.Chromecast:
        try:
            chromecast.wait()
            print("Successfully connected to Chromecast")
            maintain()
        except:
            print("Failed to connect to Chromecast")
            reconnect(1)
    else:
        print(chromecast)
        reconnect(0)

init()
