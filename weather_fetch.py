import requests

def get_weather_data(api_key, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_condition = data["weather"][0]["main"]
        temperature = data["main"]["temp"]
        return weather_condition, temperature
    else:
        raise Exception(f"Error fetching weather data: {response.json().get('message', 'Unknown error')}")

# Example usage
if __name__== "_main_":
    API_KEY = "4106c2238201b371f6b9501fdfe73099"  # Your API key
    LAT =17.366   # Latitude for Hyd
    LON = 78.476  # Longitude for Hyd

    weather, temp = get_weather_data(API_KEY, LAT, LON)
    print(f"Weather: {weather}, Temperature: {temp}°C")