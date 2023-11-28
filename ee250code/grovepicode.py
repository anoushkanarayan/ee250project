from flask import Flask, jsonify, render_template
import requests
import random
import sys
#from io import StringIO
import time

app = Flask(__name__)

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

print("Running...")
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
date = str(date)
full_date = "2023-" + "12-" + date
if len(date) < 2:
    full_date = "2023-" + "12-" + "0" + date
DATE = full_date 
#date format: year-month-day

def get_show(show):
    show_names = []
    params = {
        "country": 'US',
        "date": DATE
    }

    response = requests.get('https://api.tvmaze.com/schedule', params)

    if response.status_code == 200: # Status: OK
        data = response.json()

        for shows in data:
            show_name = shows['show']['name']
            #print(show_name)
            show_names.append(show_name)

    else:
        print('error: got response code %d' % response.status_code)
        print(response.text)
        return 0.0, 0.0
    
    return show_names

def print_shows_init():
    date = DATE
    show_list = get_show(date)
    shows_formatted = "<br>".join(show_list)
    
    output = "Showing on {date}: <br>{shows}".format(date=date, shows=shows_formatted)
    #print(output.format(date = date, shows = show_list))
    return output


SHOW_APP = {
    'name': 'DATE',
    'init': print_shows_init
}

@app.route('/')
def index():
    return render_template('index.html', output=print_shows_init())

# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)