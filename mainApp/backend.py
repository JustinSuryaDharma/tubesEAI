from datetime import datetime
from flask import Flask, jsonify, request, render_template, url_for
from external import get_coordinates, get_local_time, get_weather

import requests

app = Flask(__name__)

# get attractions
def filtered_attr(city):
  response_attraction = requests.get(f'http://localhost:3000/filterattractions?location={city}')
  return response_attraction.json()

# get article
def filtered_article(city):
  response_article = requests.get(f'http://127.0.0.1:5500/filterart?location={city}')
  return response_article.json()

# get city information
def city_info(city):
  response_city = requests.get(f'https://nominatim.openstreetmap.org/search?q={city}&format=json')
  return response_city.json()

# app routes

@app.route('/')
def show_index():
    return render_template('index.html')

@app.route('/search')
def search_city():
    city = request.args.get('location')
    return render_template('search.html')

  
@app.route('/tourism')
def get_attraction():
    city = request.args.get('location')
    
    url = "http://localhost:5000/flights/to/{}".format(city)
    headers = {
        "Authorization": "justin",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    flight=response.json()
    flight=flight['data']
    if city:
        attraction_info = filtered_attr(city)
        article_info = filtered_article(city)
        # lat, lon = get_coordinates(city)
        # local_time = get_local_time(lat, lon)[0]
        # weather = get_weather(lat, lon)
        combined_info = {
          "attraction": attraction_info,
          "articles": article_info
        }
        return render_template('article.html', data_city=combined_info, data=flight, datetime=datetime, siti=city, 
                            #    time=local_time, air=weather
                               )
    else:
        return jsonify({'error': 'Location parameter is required'}), 400


@app.route('/post')
def show_post():
    city = request.args.get('location')
    article_info = filtered_article(city)
    return render_template('post.html',siti=city, article_info=article_info)

@app.route('/flights')
def home():
    return render_template('template.html')


@app.route('/submit', methods=['POST'])
def search():
        departure = str(request.form['departure'])
        destination = str(request.form['destination'])
        date = str(request.form['date'])
        if departure and destination and date:
            url = "http://localhost:5000/flights/from/{}/to/{}/on/{}".format(departure, destination, date)
            headers = {
                "Authorization": "justin",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                flight=response.json()
                flight=flight['data']
                return render_template('nyobaclick.html', data=flight,datetime=datetime)
                # Do something with the data
            else:
                print("Error:", response.status_code)
        elif departure and destination and not date:
            url = "http://localhost:5000/flights/from/{}/to/{}".format(departure, destination)
            headers = {
                "Authorization": "justin",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                flight=response.json()
                flight=flight['data']
                return render_template('nyobaclick.html', data=flight,datetime=datetime)
                # Do something with the data
            else:
                print("Error:", response.status_code)
        elif departure and not destination and date:
            url = "http://localhost:5000/flights/from/{}/on/{}".format(departure, date)
            headers = {
                "Authorization": "justin",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                flight=response.json()
                flight=flight['data']
                return render_template('nyobaclick.html', data=flight, datetime=datetime)
                # Do something with the data
            else:
                print("Error:", response.status_code) 
        elif departure and not destination and not date:
            url = "http://localhost:5000/flights/from/{}".format(departure)
            headers = {
                "Authorization": "justin",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                flight=response.json()
                flight=flight['data']
                return render_template('nyobaclick.html', data=flight, datetime=datetime)
                # Do something with the data
            else:
                print("Error:", response.status_code)   
        elif not departure and destination and date:
            url = "http://localhost:5000/flights/to/{}/on/{}".format(destination, date)
            headers = {
                "Authorization": "justin",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                flight=response.json()
                flight=flight['data']
                return render_template('nyobaclick.html', data=flight, datetime=datetime)
                # Do something with the data
            else:
                print("Error:", response.status_code) 
        elif not departure and destination and not date:
            url = "http://localhost:5000/flights/to/{}".format(destination)
            headers = {
                "Authorization": "justin",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                flight=response.json()
                flight=flight['data']
                return render_template('nyobaclick.html', data=flight, datetime=datetime)
                # Do something with the data
            else:
                print("Error:", response.status_code) 
        elif not departure and not destination and date:
            url = "http://localhost:5000/flights/on/{}".format(date)
            headers = {
                "Authorization": "justin",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                flight=response.json()
                flight=flight['data']
                return render_template('nyobaclick.html', data=flight, datetime=datetime)
                # Do something with the data
            else:
                print("Error:", response.status_code)
        elif not departure and not destination and not date:
            url = "http://localhost:5000/flights".format(date)
            headers = {
                "Authorization": "justin",
                "Content-Type": "application/json"
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                flight=response.json()
                flight=flight['data']
                return render_template('nyobaclick.html', data=flight, datetime=datetime)
                # Do something with the data
            else:
                print("Error:", response.status_code)

@app.route('/flights/<kode_penerbangan>')
def detail(kode_penerbangan):
    url = "http://localhost:5000/flights/{}".format(kode_penerbangan)
    headers = {
                "Authorization": "justin",
                "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        flight=response.json()
        flight=flight['data']
        return render_template('detail_pemesanan.html', data=flight, datetime=datetime)
                # Do something with the data
    else:
        print("Error:", response.status_code)   

@app.route('/booking', methods=['POST'])
def book():
    total_harga = request.form.get('hiddenTotalHarga')
    kode_penerbangan = request.form.get('hiddenKodePenerbangan')
    jumlah_tiket = request.form.get('jumlahTiket')
    nik = request.form.get('nik')
    email = request.form.get('email')

    if not (total_harga and kode_penerbangan and jumlah_tiket and nik and email):
        return "Invalid form data", 400

    url = "http://localhost:5000/bookings/{}/{}/{}/{}/{}".format(total_harga,kode_penerbangan,jumlah_tiket,nik,email)
    headers = {
            "Authorization": "justin",
            "Content-Type": "application/json"
        }
    response = requests.post(url, headers=headers)

    return render_template('index.html', response=response)

@app.route('/cityinfo', methods=['POST'])
def get_city_info():
    city = request.args.get('location')
    if not city:
        return "City name is required", 400
    
    try:
        lat, lon = get_coordinates(city)
        local_time = get_local_time(lat, lon)
        weather = get_weather(lat, lon)
        return jsonify({
            'city': city,
            'latitude': lat,
            'longitude': lon,
            'local_time': local_time,
            'air': weather
        })
    except Exception as e:
        return str(e), 500

if __name__ =="__main__":
  app.run(debug=True, port=5009)