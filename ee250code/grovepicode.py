import requests
import random
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

while button_pressed == False:
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

        time.sleep(0.3)

    except KeyboardInterrupt:
        break

    except IOError:
        print("Error")

# variable 'date' comes from grovepi code
full_date = "2023-" + "12-" + str(date)
DATE = full_date 
#date format: year-month-day


def get_show(show):
    params = {
        "country": 'US',
        "date": DATE
    }

    response = requests.get('https://api.tvmaze.com/schedule', params)

    if response.status_code == 200: # Status: OK
        data = response.json()

        for shows in data:
            show_name = shows['show']['name']
            print(show_name)
       
        '''
       
        # Extracts the summary from the data
        output = (data["summary"])
        #print(output) 
        return output
        '''

    else:
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return 0.0, 0.0

def print_shows_init():
    date = DATE
    show_list = get_show(date)
    
    
    output = "{date} show list: {shows}"
    #print(output.format(date = date, shows = show_list))
    output = output.format(date = date, shows = show_list)

    return output


SHOW_APP = {
    'name': 'DATE',
    'init': print_shows_init
}


if __name__ == '__main__':
    print_shows_init()

