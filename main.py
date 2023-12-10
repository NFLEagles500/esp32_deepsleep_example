'''
Must be used on QTpy ESP32 Pico
References:
    https://learn.adafruit.com/adafruit-qt-py-esp32-pico/overview
    For esp32 only micropython machine.deepsleep and machine.lightsleep:
    https://www.engineersgarage.com/micropython-esp32-modem-light-deep-sleep-modes-timer-external-touch-wake-up/#:~:text=There%20are%20two%20external%20%E2%80%9Cwake,of%20its%20capacitive%20touch%20pins.
    https://docs.micropython.org/en/latest/esp32/quickref.html
'''
import time
import uos
import machine
from neopixel import NeoPixel
import esp32

resetCauseNames = ['PWRON_RESET','HARD_RESET','WDT_RESET','DEEPSLEEP_RESET','SOFT_RESET','BROWN_OUT_RESET']
wakeReasons = ['PIN_WAKE','EXT0_WAKE','EXT1_WAKE','TIMER_WAKE','TOUCHPAD_WAKE','ULP_WAKE']

resetCause = next(item for item in resetCauseNames if machine.reset_cause() == getattr(machine, item))
print(f'Reset reason: {resetCause}')

if resetCause == 'DEEPSLEEP_RESET':
    wakeReason = next(item for item in wakeReasons if machine.wake_reason() == getattr(machine, item))
    print(f'woke up from a deep sleep because {wakeReason}')

power_pin = machine.Pin(8, machine.Pin.OUT)  # NeoPixel power is on pin 8
power_pin.on()  # Enable the NeoPixel Power
interrupt_pin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)
pin = machine.Pin(5, machine.Pin.OUT)  # Onboard NeoPixel is on pin 5
np = NeoPixel(pin, 1)  # create NeoPixel driver on pin 5 for 1 pixel
print(f'Reset Cause: {machine.reset_cause()} Wake Reason: {machine.wake_reason()}')
blink_iter = 1
while blink_iter > 0:
    np.fill((0, 0, 150))  # Set the NeoPixel blue
    np.write()  # Write data to the NeoPixel
    time.sleep(0.5)  # Pause for 0.5 seconds
#    np.fill((0, 0, 0))  # Turn the NeoPixel off
#    np.write()  # Write data to the NeoPixel
    time.sleep(0.5)  # Pause for 0.5 seconds
    blink_iter = blink_iter - 1
#deepsleep will NOT process interrupts, it will only restart the microcontroller
#interrupt_pin.irq(trigger=Pin.IRQ_RISING, handler=wake_up)

#Use esp32.wake_on_ext0 to allow a GPIO pin change wake it
esp32.wake_on_ext0(interrupt_pin,esp32.WAKEUP_ANY_HIGH)
machine.deepsleep(5000)
