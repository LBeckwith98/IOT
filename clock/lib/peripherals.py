import gpiozero

# Global used for GPIO pin, can be changed
RELAY_PIN = 22
BUTTON_LIGHT_PIN = 17
BUTTON_ALARM_PIN = 27

# create relay object
# triggered by going high
relay = gpiozero.OutputDevice(RELAY_PIN, active_high=True, initial_value=False)
button_light = gpiozero.Button(BUTTON_LIGHT_PIN, pull_up=False,bounce_time=.1)
button_alarm = gpiozero.Button(BUTTON_ALARM_PIN, pull_up=False,bounce_time=.1)

def set_relay(status):
    pass
    if status:
        relay.on()
    else:
        relay.off()

def toggle_relay():
    relay.toggle()
