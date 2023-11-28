import requests
import sys
import time
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')

import grovepi
import grove_rgb_lcd as lcd

# Rotary Encoder setup
#rotary_encoder_pin = 2
#grovepi.pinMode(rotary_encoder_pin, "INPUT")
rotary_encoder_pin_A = 2  # Connect encoder pin A to D2 on the GrovePi board
rotary_encoder_pin_B = 3  # Connect encoder pin B to D3 on the GrovePi board
grovepi.pinMode(rotary_encoder_pin_A, "INPUT")
grovepi.pinMode(rotary_encoder_pin_B, "INPUT")

# Button setup
button_pin = 4
grovepi.pinMode(button_pin, "INPUT")

# LCD backlight setup
lcd.setRGB(0, 255, 0)  # Set initial backlight color to green

# Initialize variables
current_value = 1
date = None
button_pressed = False

def update_lcd(value):
    lcd.setText("Day of Dec: {}".format(value))

while True:
    try:
        # Read the rotary encoder value
        #rotary_value = grovepi.digitalRead(rotary_encoder_pin)

        # Map the rotary value to the desired range (1-31)
        #current_value = int((rotary_value / 1023.0)) + 1 # * 30

        # Read the rotary encoder values
        rotary_value_A = grovepi.digitalRead(rotary_encoder_pin_A)
        rotary_value_B = grovepi.digitalRead(rotary_encoder_pin_B)

        # Check for changes in encoder values
        if rotary_value_A == 0 and rotary_value_B == 1:
            # Encoder is turned clockwise
            current_value = min(mapped_max, current_value + 1)
        elif rotary_value_A == 1 and rotary_value_B == 0:
            # Encoder is turned counterclockwise
            current_value = max(mapped_min, current_value - 1)

        # Map the value to the desired range
        #current_value = map_value(current_value, mapped_min, mapped_max, analog_min, analog_max)

        # Update the value
        update_value(current_value)
        update_lcd(current_value)

        # Check if the button is pressed
        button_state = grovepi.digitalRead(button_pin)
        if button_state == 1 and not button_pressed:
            # Button is pressed for the first time
            date = current_value
            button_pressed = True
            print("Day of December:", date)

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

