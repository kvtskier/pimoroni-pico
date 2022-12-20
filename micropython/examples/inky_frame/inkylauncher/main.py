from picographics import PicoGraphics, DISPLAY_INKY_FRAME_4 as DISPLAY  # 4.0"
import gc
import time
from machine import reset
import inky_helper as ih

# Create a secrets.py with your Wifi details to be able to get the time
#
# secrets.py should contain:
# WIFI_SSID = "Your WiFi SSID"
# WIFI_PASSWORD = "Your WiFi password"

# Setup for the display.
graphics = PicoGraphics(DISPLAY)
WIDTH, HEIGHT = graphics.get_bounds()
graphics.set_font("bitmap8")


def launcher():
    # Draws the menu
    graphics.set_pen(1)
    graphics.clear()
    graphics.set_pen(0)

    graphics.set_pen(5)
    graphics.rectangle(0, 20, WIDTH, 50)
    graphics.set_pen(0)
    graphics.text("Launcher", 245, 30, WIDTH, 4)

    graphics.set_pen(4)
    graphics.rectangle(30, 80, WIDTH - 100, 50)
    graphics.set_pen(1)
    graphics.text("A. NASA Picture Of the Day", 35, 95, 600, 3)

    graphics.set_pen(6)
    graphics.rectangle(30, 140, WIDTH - 150, 50)
    graphics.set_pen(1)
    graphics.text("B. Word Clock", 35, 155, 600, 3)

    graphics.set_pen(2)
    graphics.rectangle(30, 200, WIDTH - 200, 50)
    graphics.set_pen(1)
    graphics.text("C. Daily Activity", 35, 215, 600, 3)

    graphics.set_pen(3)
    graphics.rectangle(30, 260, WIDTH - 250, 50)
    graphics.set_pen(1)
    graphics.text("D. Headlines", 35, 275, 600, 3)

    graphics.set_pen(0)
    graphics.rectangle(30, 320, WIDTH - 300, 50)
    graphics.set_pen(1)
    graphics.text("E. Random Joke", 35, 335, 600, 3)

    graphics.set_pen(7)
    graphics.rectangle(WIDTH - 100, 80, 70, 50)
    graphics.rectangle(WIDTH - 150, 140, 120, 50)
    graphics.rectangle(WIDTH - 200, 200, 170, 50)
    graphics.rectangle(WIDTH - 250, 260, 220, 50)
    graphics.rectangle(WIDTH - 300, 320, 270, 50)

    graphics.update()

    # Now we've drawn the menu to the screen, we wait here for the user to select an app.
    # Then once an app is selected, we set that as the current app and reset the device and load into it.

    # You can replace any of the included examples with one of your own,
    # just replace the name of the app in the line "ih.update_last_app("nasa_apod")"

    while True:
        if ih.inky_frame.button_a.read():
            ih.button_a_led.on()
            ih.update_state("nasa_apod")
            time.sleep(0.5)
            reset()
        if ih.inky_frame.button_b.read():
            ih.button_b_led.on()
            ih.update_state("word_clock")
            time.sleep(0.5)
            reset()
        if ih.inky_frame.button_c.read():
            ih.button_c_led.on()
            ih.update_state("daily_activity")
            time.sleep(0.5)
            reset()
        if ih.inky_frame.button_d.read():
            ih.button_d_led.on()
            ih.update_state("news_headlines")
            time.sleep(0.5)
            reset()
        if ih.inky_frame.button_e.read():
            ih.button_e_led.on()
            ih.update_state("random_joke")
            time.sleep(0.5)
            reset()


# Turn any LEDs off that may still be on from last run.
ih.clear_button_leds()
ih.led_warn.off()

if ih.pressed() == ih.inky_frame.button_e:
    launcher()

ih.clear_button_leds()

if ih.file_exists("state.json"):
    # Loads the JSON and launches the app
    ih.load_state()
    ih.launch_app(ih.state['run'])

    # Passes the the graphics object from the launcher to the app
    ih.app.graphics = graphics
    ih.app.WIDTH = WIDTH
    ih.app.HEIGHT = HEIGHT

else:
    launcher()

try:
    from secrets import WIFI_SSID, WIFI_PASSWORD
    ih.network_connect(WIFI_SSID, WIFI_PASSWORD)
except ImportError:
    print("Create secrets.py with your WiFi credentials")

# Get some memory back, we really need it!
gc.collect()

# The main loop executes the update and draw function from the imported app,
# and then goes to sleep ZzzzZZz

file = ih.file_exists("state.json")

print(file)

while True:
    ih.app.update()
    ih.app.draw()
    ih.sleep(ih.app.UPDATE_INTERVAL)
