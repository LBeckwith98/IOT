import lib.wunderAPI as wunder
import lib.SoftwareTimer as SoftwareTimer
import lib.server as serverLib
import time

REFRESH_RATE = 4

refreshTimer = SoftwareTimer.OneShotTimer(REFRESH_RATE)
refreshTimer.start()

server = serverLib.Server()
print('initialized')
while 1:
    time.sleep(.25)
    if refreshTimer.expired():
        refreshTimer.start()
        print("active == " + str(server.connDict["ALARM_CLOCK"]["active"]))
        if server.refreshConnection() > 1:

            #cmd = wunder.pollWunder()
            #print(cmd)

            # tmp manual entering #
            cmd = [None,None,None,None]
            cmd[0] = "ALARM_CLOCK"
            cmd[1]= "UPDATE_TIME"
            cmd[2] = str(input("Hr: "))
            cmd[3]= str(input("Min: "))

            ## SEND MESSAGE ##

            if cmd[0] == "ALARM_CLOCK":
                sent = server.sendCmdTo("ALARM_CLOCK", cmd[1:])
                tries = 0
                while not sent and tries < 5:
                    server.refreshConnection()
                    tries = tries + 1
                    sent = server.sendCmdTo("ALARM_CLOCK", cmd[1:])

