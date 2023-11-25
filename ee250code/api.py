import requests
import random

# TV show API: https://www.tvmaze.com/api#show-search

date = input("enter a day in December: ")

# variable 'date' comes from grovepi code
full_date = "2023-" + "12-" + date
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
    
    
    for show in show_list:

        output = "{date} summary: {shows}"
        print(output.format(date = date, shows = show))
        output = output.format(date = date, shows = show)

    return output


SHOW_APP = {
    'name': 'DATE',
    'init': print_shows_init
}


if __name__ == '__main__':
    print_shows_init()
