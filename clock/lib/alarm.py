from datetime import datetime, time, timedelta, date
from threading import Thread

from pygame import mixer  # Load the required library

import peripherals

pre_alarm = 10
post_alarm = 5
REFRESH_RATE = 5  # how long too wait between checking for time and messages


class AlarmClock(Thread):


    def __init__(self,):
        Thread.__init__(self)
        self.alarm_hour = 21
        self.alarm_minute = 57
        self.active = True
        self.state = "OFF"


    def soundAlarm(self):
        # start music
        mixer.init()
        mixer.music.load('~/automation/alarm_tone.mp3')
        mixer.music.play()

        count = 0
        while count < 5:
            # repeat 5 times unless button is pressed
            if mixer.music.get_pos() == -1:
                count += 1

            if peripherals.button_alarm.is_pressed:
                mixer.music.stop()
                break


    def checkAlarm(self):
        # FSM:
        # States: OFF, LIGHT_ON, ALARM_ON

        # Checks current time vs alarm time
        alarm_time = datetime.combine(date.today(), time(self.alarm_hour, self.alarm_minute))

        #### FSM ####
        now_time = datetime.now()
        # STATE 1: everything is off
        if self.state == "OFF":
            if now_time >= alarm_time - timedelta(minutes=pre_alarm) and now_time <= alarm_time:
                peripherals.set_relay(True)
                self.state = "LIGHT_ON"

        # STATE 2: light has been triggered
        if self.state == "LIGHT_ON":
            if now_time >= alarm_time and now_time <= alarm_time + timedelta(minutes=1) :
                #self.sound_alarm()
                self.state = "ALARM_ON"

        # STATE 3: alarm has been triggered
        if self.state == "ALARM_ON":
            if now_time >= alarm_time + timedelta(minutes=post_alarm):
                peripherals.set_relay(False)
                self.state = "OFF"
