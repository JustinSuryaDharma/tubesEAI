import requests

def get_coordinates(city_name):
    city_name = city_name.lower()
    url_city = f"https://world-citiies-api.p.rapidapi.com/cities/{city_name}"
    headers_city = {
      "X-RapidAPI-Key": "3350ea7d8bmsh19df7418eed4043p1b3356jsnc8494bf9670d",
      "X-RapidAPI-Host": "world-citiies-api.p.rapidapi.com"
    }
    response_city = requests.get(url_city, headers=headers_city)
    data = response_city.json()
    if data:
      coordinates = data[0]['Coordinates']
      lat, lon = map(float, coordinates.split(','))
      return lat, lon
    else:
      raise Exception(f"City {city_name} not found")

def get_local_time(lat, lon):
    url_time = "https://geocodeapi.p.rapidapi.com/GetNearestCities"

    querystring = {"latitude":str(lat),"longitude":str(lon),"range":"0"}

    headers = {
      "X-RapidAPI-Key": "3350ea7d8bmsh19df7418eed4043p1b3356jsnc8494bf9670d",
      "X-RapidAPI-Host": "geocodeapi.p.rapidapi.com"
    }

    response_time = requests.get(url_time, headers=headers, params=querystring)
    return response_time.json()

def get_weather(lat, lon):
    url = "https://air-quality-by-api-ninjas.p.rapidapi.com/v1/airquality"
    querystring = {"lat":str(lat),"lon":str(lon)}
    headers = {
      "X-RapidAPI-Key": "3350ea7d8bmsh19df7418eed4043p1b3356jsnc8494bf9670d",
      "X-RapidAPI-Host": "air-quality-by-api-ninjas.p.rapidapi.com"
    }
    response_air = requests.get(url, headers=headers, params=querystring)
    return response_air.json()
