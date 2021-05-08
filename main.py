from config import *
import requests
from twilio.rest import Client

weather_params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": API_KEY,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_ENDPOINT, weather_params)
response.raise_for_status()

print(f"HTTP Status Code: {response.status_code}")

weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

weather_cond = ["Rain" if weather_data["hourly"][i]
                ["weather"][0]["id"] < 700 else "Dry" for i in range(12)]

if "Rain" in weather_cond:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages \
        .create(
            body="It's going to rain today. Remember to bring an ☔",
            from_=PHONE_NUMBER_01,
            to=PHONE_NUMBER_02
        )
    print(message.status)
