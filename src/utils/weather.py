from os import environ
import requests

openweathermap_api_key = environ.get('OPENWEATHERMAP_API_KEY', default = 0)

def lookup(user_search):

    # Check for and convert zip/post code to latitude/longitutde
    # https://openweathermap.org/api/geocoding-api#direct_zip_how
    if user_search.isnumeric():
        if int(float(user_search)) > 0 and int(float(user_search)) < 100000: # Zipcode formatting
            url = f'http://api.openweathermap.org/geo/1.0/zip?zip={user_search}&appid={openweathermap_api_key}'
            response = requests.get(url)
            data = response.json()
            lat = float(data['lat'])
            lon = float(data['lon'])

    # Convert location city/area name to latitude/longitutde
    # https://openweathermap.org/api/geocoding-api#direct_name_how
    else:
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={user_search}&limit=1&appid={openweathermap_api_key}'
        response = requests.get(url)
        data = response.json()
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])

    # Get current weather data for a latitude/longitutde
    # https://openweathermap.org/current#geo
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={openweathermap_api_key}'
    response = requests.get(url)
    data = response.json()

    temperature_data = data['main']
    rounded_temperature = int(round(temperature_data["temp"],0))
    
    weather_data = data['weather'][0]
    sky_description = weather_data["description"]
    
    location = data["name"]

    msg = f'{rounded_temperature}°F with {sky_description} in {location} right now.'
    return msg

# Example of second function
def test():
    return 0

# Used for executing directly when testing
if __name__ == "__main__":
    weather_to_check = lookup('11023')
    print(weather_to_check, flush=True)
