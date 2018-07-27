import lib.alarm as alarm
import lib.client as client
import lib.peripherals as peripherals
import lib.SoftwareTimer as SoftwareTimer
import time


REFRESH_RATE = 5

myClock = alarm.AlarmClock()

client = client.Client()
while not client.connect("192.168.2.3", 12345): time.sleep(REFRESH_RATE)

refreshTimer = SoftwareTimer.OneShotTimer(REFRESH_RATE)
refreshTimer.start()

c = 0
while(True):
    ## check alarm ##
    myClock.checkAlarm()
    if refreshTimer.expired():
        c = c + 1
        refreshTimer.start()
        if client.refreshConnect():

            ## CHECK FOR MSG ##
            cmd = client.receiveCmd()
            if cmd != '':
                print(cmd)
                if cmd[0] == "UPDATE_TIME":
                    myClock.alarm_hour = int(cmd[1])
                    myClock.alarm_minute = int(cmd[2])
                    print('Alarm time updated to {}:{}'.format(cmd[1], cmd[2]))


    ## CHECKING BUTTONS ###
    if peripherals.button_light.is_pressed and released:
           peripherals.toggle_relay()
           released = False

    if not peripherals.button_light.is_pressed:
        released = True