import streamlit as st
import datetime
import requests

algoliaPlacesApiAppId = 'MM1BWXHPTD'
algoliaPlacesApiKey = '5543b7a01315f7b399e9663ad49a85bd'




'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')
'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
'''

columns = st.columns(2)

pickup_date = columns[0].date_input("For which day do you want to schedule the ride?", datetime.date(2019, 7, 6))
pickup_time = columns[1].time_input("For which time do you want to schedule the ride?", datetime.time(11,00,00))

pickup_datetime = str(pickup_date) + " " + str(pickup_time)

url = 'https://places-dsn.algolia.net/1/places/query'

pickup_address = columns[1].text_input('Where are you gonna be picked up?',
                                       'Empire State Building')

response = requests.get(url, {"query": pickup_address})

pickup_geoloc = response.json()["hits"][0]["_geoloc"]

pickup_longitude = pickup_geoloc["lng"]
pickup_latitude = pickup_geoloc["lat"]

dropoff_longitude = columns[0].text_input('What is your dropoff longitude?',
                                  '-73.984365')

dropoff_latitude = columns[1].text_input('What is your dropoff latitude?', '40.769802')

passenger_count = st.text_input("How many passengers will you be", "1")

'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

url = 'https://taxifare-uvj5vais2q-ew.a.run.app/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown(
        'Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...'
    )
'''

2. Let's build a dictionary containing the parameters for our API...
'''

params = {
    "key": "key",
    "pickup_datetime": pickup_datetime,
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}

'''
3. Let's call our API using the `requests` package...
'''

response = requests.get(url, params=params)

'''
4. Let's retrieve the prediction from the **JSON** returned by the API...

'''

prediction = response.json()["prediction"][0]

'''

## Finally, we can display the prediction to the user
'''

st.write(f"Your fare will cost ${round(prediction, 2)}")
