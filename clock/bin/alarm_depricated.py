import SoftwareTimer
from datetime import datetime, time, timedelta, date
from pygame import mixer  # Load the required library
from threading import Thread

from clock.lib import peripherals

pre_alarm = 10
post_alarm = 5
REFRESH_RATE = 5  # how long too wait between checking for time and messages


class alarm_clock(Thread):

    def __init__(self, messageQueue):
        Thread.__init__(self)
        self.queue = messageQueue
        self.alarm_hour = 22
        self.alarm_minute = 20
        self.active = True

        # create software timer
        self.refreshTimer = SoftwareTimer.OneShotTimer(REFRESH_RATE)


    def sound_alarm(self):
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

    def run(self):
        # start time
        self.refreshTimer.start()

        # FSM:
        # States: OFF, LIGHT_ON, ALARM_ON
        state = "OFF"

        # Checks current time vs alarm time
        alarm_time = datetime.combine(date.today(), time(self.alarm_hour, self.alarm_minute))
        while True:
            # Check if timer has expired
            if self.refreshTimer.expired():
                # restart timer
                self.refreshTimer.start()

                # Check if update received a message
                if not self.queue.empty():
                    msg = self.queue.get(False)
                    if msg == 'update':
                        self.alarm_hour = int(self.queue.get(True))
                        self.alarm_minute = int(self.queue.get(True))
                        alarm_time = datetime.combine(date.today(), time(self.alarm_hour, self.alarm_minute))


                #### FSM ####
                now_time = datetime.now()

                # STATE 1: everything is off
                if state == "OFF":
                    if now_time >= alarm_time - timedelta(minutes=pre_alarm) and now_time <= alarm_time:
                        peripherals.set_relay(True)
                        state = "LIGHT_ON"

                # STATE 2: light has been triggered
                if state == "LIGHT_ON":
                    if now_time >= alarm_time and now_time <= alarm_time + timedelta(minutes=1) :
                        self.sound_alarm()
                        state = "ALARM_ON"

                # STATE 3: alarm has been triggered
                if state == "ALARM_ON":
                    if now_time >= alarm_time + timedelta(minutes=post_alarm):
                        peripherals.set_relay(False)
                        state = "OFF"
