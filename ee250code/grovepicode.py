import requests
import sys
import time
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')

import grovepi
import grove_rgb_lcd as lcd

# Rotary Encoder setup
rotary_encoder_pin = 2
grovepi.pinMode(rotary_encoder_pin, "INPUT")

# Button setup
button_pin = 3
grovepi.pinMode(button_pin, "INPUT")

# LCD backlight setup
lcd.setRGB(0, 255, 0)  # Set initial backlight color to green

# Initialize variables
current_value = 1
date = None
button_pressed = False

def update_lcd(value):
    lcd.setText("Value: {}".format(value))

while True:
    try:
        # Read the rotary encoder value
        rotary_value = grovepi.analogRead(rotary_encoder_pin)

        # Map the rotary value to the desired range (1-31)
        current_value = int((rotary_value / 1023.0) * 30) + 1

        # Update LCD with current value
        update_lcd(current_value)

        # Check if the button is pressed
        button_state = grovepi.digitalRead(button_pin)
        if button_state == 1 and not button_pressed:
            # Button is pressed for the first time
            date = current_value
            button_pressed = True
            print("Value frozen and stored in 'date':", date)

        elif button_state == 0 and button_pressed:
            # Button is released
            button_pressed = False

        time.sleep(0.1)

    except KeyboardInterrupt:
        break

    except IOError:
        print("Error")

# Clean up
lcd.setText("")
lcd.setRGB(0, 0, 0)  # Turn off backlight
