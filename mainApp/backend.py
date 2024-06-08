from datetime import datetime
from flask import Flask, jsonify, request, render_template, url_for
from external import get_coordinates, get_local_time, get_weather

import requests

app = Flask(__name__)

city = None

# get attractions
def filtered_attr(city):
  response_attraction = requests.get(f'http://localhost:3000/filterattractions?location={city}')
  return response_attraction.json()

# get article
def filtered_article(city):
  response_article = requests.get(f'http://127.0.0.1:5500/filterart?location={city}')
  return response_article.json()

# get attractions by name
def filtered_attr_name(name):
  response_nameattraction = requests.get(f'http://localhost:3000/nameattractions?name={name}')
  return response_nameattraction.json()

# get city information
def city_info(city):
  response_city = requests.get(f'https://nominatim.openstreetmap.org/search?q={city}&format=json')
  return response_city.json()

# get flight information
def flight_info(city):
    url = "http://localhost:5000/flights/to/{}".format(city)
    headers = {
        "Authorization": "justin",
        "Content-Type": "application/json"
    }
    response_flight = requests.get(url, headers=headers)
    return response_flight.json()

# get atttraction ticket (external source)
def filtered_ticket(city):
    response_ticket = requests.get(f'http://localhost:3001/lokasi/{city}')
    return response_ticket.json()

def get_ticket_data():
    response_all_ticket = requests.get('http://localhost:3001/tiket')
    return response_all_ticket.json()

def get_ticket_by_name(name):
    response = requests.get(f'http://localhost:3001/tiket/nama/{name}')
    if response.status_code == 200:
        return response.json()
    else:
        return None

# app routes
@app.route('/')
def show_index():
    return render_template('index.html')

@app.route('/search')
def search_city():
    return render_template('search.html')
  
@app.route('/tourism')
def get_attraction():
    global city 
    city = request.args.get('location')
    
    flight=flight_info(city)
    flight=flight['data']
    if city:
        attraction_info = filtered_attr(city)
        article_info = filtered_article(city)
        # lat, lon = get_coordinates(city)
        # local_time = get_local_time(lat, lon)[0]
        # weather = get_weather(lat, lon)
        attraction_ticket = filtered_ticket(city)
        combined_info = {
          "attraction": attraction_info,
          "articles": article_info
        }
        return render_template('article.html', data_city=combined_info, data=flight, datetime=datetime, siti=city, ticket=attraction_ticket
                               #    time=local_time, air=weather
                               )
    else:
        return jsonify({'error': 'Location parameter is required'}), 400

@app.route('/detail/<nama_wisata>')
def show_ticket(nama_wisata):
    ticket_details = get_ticket_by_name(nama_wisata)
    attraction = filtered_attr_name(nama_wisata)
    if ticket_details and attraction:
        return render_template('detail_ticket.html', data=ticket_details[0], atraksi=attraction[0])
    else:
        return "Attraction not found", 404

@app.route('/tiket/beli/<int:id>', methods=['POST'])
def beli_tiket(id):
    data = request.get_json()
    jumlah = data.get('jumlah')
    ticket_data = get_ticket_data()
    if id not in ticket_data:
        return jsonify({"success": False, "message": "Tiket tidak ditemukan"}), 404

    tiket = ticket_data[id]

    if tiket['stock'] < jumlah:
        return jsonify({"success": False, "message": "Stok tidak cukup"}), 400

    # Update stock
    tiket['stock'] -= jumlah

    # Here you would add your database update logic to save the new stock amount
    return jsonify({"success": True, "message": "Pembelian tiket berhasil"}), 200

@app.route('/confirmationTicket')
def confirmation_ticket():
    return "Pembelian tiket berhasil! Ini adalah halaman konfirmasi."

    
@app.route('/post')
def show_post():
    global city
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