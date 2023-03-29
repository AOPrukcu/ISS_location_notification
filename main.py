import requests
from datetime import  datetime
import smtplib
import time
starttime= time.time()

MY_EMAIL = "YOUR EMAİL"
MY_PASSWORD = "YOUR PASSWORD"
RECEİVER = "RECEİVER EMAİL"

MY_LAT = 35.095192
MY_LONG = 33.203430

while True:
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()

    longitude  = float(response.json()["iss_position"]["longitude"])
    latitude = float(response.json()["iss_position"]["latitude"])

    iss_position = (longitude, latitude)
    print(iss_position)

    parameters = {
        "formatted":0,
        "lat":MY_LAT,
        "lng":MY_LONG,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    print(sunrise)
    print(sunset)

    time_now = int(datetime.now().hour)
    print(time_now)

    if abs(MY_LAT-iss_position[0]) and abs(MY_LONG-iss_position[1]) <= 5:
        if time_now > sunrise and time_now < sunset:
            sky = "its sunny"
            with smtplib.SMTP("smtp.live.com") as connection:
                connection.starttls()
                connection.login(MY_EMAIL, MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=MY_EMAIL,
                    msg=f"Subject:iss is near you!\n\nlook out\niss cordinations{iss_position} and {sky}"
            )
        time.sleep(60)
