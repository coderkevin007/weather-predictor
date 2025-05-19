import streamlit as st
import requests
from datetime import datetime
from PIL import Image
from io import BytesIO

API_KEY = "06c921750b9a82d8f5d1294e1586276f"

def get_weather_data(city):
    current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}"

    current_data = requests.get(current_url).json()
    forecast_data = requests.get(forecast_url).json()
    return current_data, forecast_data

def kelvin_to_celsius(kelvin):
    return int(kelvin - 273.15)

def get_icon_url(icon_code):
    return f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

# Streamlit UI
st.set_page_config(page_title="Weather Predictor App", layout="centered")
st.title("🌍 Weather Predictor App")

place = st.text_input("Enter place name:", "")

if st.button("Get Forecast") or place:
    if place.strip() == "":
        st.warning("Please enter a valid place name.")
    else:
        current_data, forecast_data = get_weather_data(place)

        if current_data.get("cod") != 200:
            st.error("City not found. Please check your input.")
        else:
            condition = current_data['weather'][0]['main']
            description = current_data['weather'][0]['description']
            icon = current_data['weather'][0]['icon']
            icon_url = get_icon_url(icon)
            temp = kelvin_to_celsius(current_data['main']['temp'])
            min_temp = kelvin_to_celsius(current_data['main']['temp_min'])
            max_temp = kelvin_to_celsius(current_data['main']['temp_max'])
            pressure = current_data['main']['pressure']
            humidity = current_data['main']['humidity']
            wind = current_data['wind']['speed']
            sunrise = datetime.utcfromtimestamp(current_data['sys']['sunrise']).strftime('%I:%M:%S %p')
            sunset = datetime.utcfromtimestamp(current_data['sys']['sunset']).strftime('%I:%M:%S %p')

            st.subheader(f"Current Weather in {place.title()}")
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(icon_url, width=80)
            with col2:
                st.markdown(f"**{description.title()}**, {temp}°C")

            st.text(f"Min Temp: {min_temp}°C\nMax Temp: {max_temp}°C")
            st.text(f"Pressure: {pressure} hPa\nHumidity: {humidity}%\nWind Speed: {wind} m/s")
            st.text(f"Sunrise: {sunrise}\nSunset: {sunset}")

            st.subheader("📅 5-Day Forecast")
            forecast_list = forecast_data['list']
            forecast_display = {}

            for item in forecast_list:
                dt_txt = item['dt_txt']
                date_str, time_str = dt_txt.split()
                if time_str == "12:00:00":
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    day_name = date_obj.strftime("%A")
                    temp = kelvin_to_celsius(item['main']['temp'])
                    desc = item['weather'][0]['description']
                    icon = item['weather'][0]['icon']
                    icon_url = get_icon_url(icon)

                    forecast_display[day_name] = {
                        "temp": temp,
                        "desc": desc,
                        "icon_url": icon_url
                    }

            for day, info in forecast_display.items():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.image(info["icon_url"], width=60)
                with col2:
                    st.markdown(f"**{day}**: {info['temp']}°C, {info['desc'].title()}")
