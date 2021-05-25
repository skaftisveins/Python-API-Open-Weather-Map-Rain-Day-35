from config import *
import requests
from twilio.rest import Client

weather_params = {
    "lat": my_lat,
    "lon": my_long,
    "appid": owm_api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(owm_endpoint, weather_params)
response.raise_for_status()

print(f"HTTP Status Code: {response.status_code}")

weather_data = response.json()

weather_cond = ["Rain" if weather_data["hourly"][i]
                ["weather"][0]["id"] < 700 else "Dry" for i in range(12)]

if "Rain" in weather_cond:
    client = Client(twilio_account_sid, twilio_auth_token)
    message = client.messages \
        .create(
            body="It's going to rain today. Remember to bring an umbrella☔",
            from_=twilio_phone_number,
            to=my_phone_number
        )
    print(message.status)

else:
    print("It looks like it's not raining today, for the next 12 hours at least..")
