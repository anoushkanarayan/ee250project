import requests
import sys
import time
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')

import grovepi
import grove_rgb_lcd as lcd

rotary_encoder_pin_A = 2 
rotary_encoder_pin_B = 3 
grovepi.pinMode(rotary_encoder_pin_A, "INPUT")
grovepi.pinMode(rotary_encoder_pin_B, "INPUT")

button_pin = 4
grovepi.pinMode(button_pin, "INPUT")

current_value = 1
date = None
button_pressed = False
lcd.setRGB(0, 255, 0)

def update_lcd(value):
    lcd.setText("Day of Dec: {}".format(value))
    print("Updated Value:", value)

while True:
    try:
        rotary_value_A = grovepi.digitalRead(rotary_encoder_pin_A)
        rotary_value_B = grovepi.digitalRead(rotary_encoder_pin_B)

        if rotary_value_A == 0 and rotary_value_B == 1:
            if current_value == 31:
                current_value = 0
            current_value = min(31, current_value + 1)

        update_lcd(current_value)

        button_state = grovepi.digitalRead(button_pin)
        if button_state == 1 and not button_pressed:
            date = current_value
            button_pressed = True
            print("Day of December:", date)

        elif button_state == 0 and button_pressed:
            button_pressed = False

        time.sleep(0.3)

    except KeyboardInterrupt:
        break

    except IOError:
        print("Error")

