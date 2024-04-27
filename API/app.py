import uuid
import hashlib
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)


# ### CONNECT DATABASE -- database used = aiven
app.config['MYSQL_HOST'] = 'libratur-database-xylamaharanii-9ca8.b.aivencloud.com'
app.config['MYSQL_USER'] = 'avnadmin'
app.config['MYSQL_PASSWORD'] = 'AVNS_8pk8_VpEMvETZuR__I4'
app.config['MYSQL_DB'] = 'tubes_eai_mysql'
app.config['MYSQL_PORT'] = 15532 
mysql = MySQL(app)



# # ### Authentication Logic
# valid_tokens = {"valid": "safety"}
# def verify_token(token):
#     return token == valid_tokens['valid']

# @app.before_request
# def authenticate():
#     token = request.headers.get('Authorization')
#     if not token or not verify_token(token):
#         return jsonify({"status_code": "401","status": "error", "message": "Unauthorized", "timestamp": datetime.now()}), 401



### DAFTAR PENERBANGAN -- GET method --
@app.route('/flights', methods=['GET'])
def get_all_flights():
    cursor = mysql.connection.cursor()
    
    # Fetch all flights
    cursor.execute('''
        SELECT Tiket_Penerbangan.kode_penerbangan, Tiket_Penerbangan.kode_pesawat, Tiket_Penerbangan.kode_maskapai, Tiket_Penerbangan.jumlah_tiket, Tiket_Penerbangan.dept_IATA, Tiket_Penerbangan.dest_IATA, Tiket_Penerbangan.dept_time, Tiket_Penerbangan.arriv_time, 
                   Tiket_Penerbangan.harga,departure_airport.nama_bandara AS departure_airport, 
                   departure_airport.nama_kota AS departure_city, 
                   departure_airport.nama_negara AS departure_country, 
                   arrival_airport.nama_bandara AS arrival_airport, 
                   arrival_airport.nama_kota AS arrival_city, 
                   arrival_airport.nama_negara AS arrival_country, 
                   Maskapai.nama_maskapai,
                   Pesawat.max_luggage
        FROM Tiket_Penerbangan
        INNER JOIN Bandara AS departure_airport ON Tiket_Penerbangan.dept_IATA = departure_airport.IATA
        INNER JOIN Bandara AS arrival_airport ON Tiket_Penerbangan.dest_IATA = arrival_airport.IATA
        INNER JOIN Maskapai ON Maskapai.kode_maskapai = Tiket_Penerbangan.kode_maskapai
        INNER JOIN Pesawat ON Pesawat.kode_pesawat = Tiket_Penerbangan.kode_pesawat
    ''')
    flights = cursor.fetchall()

    # If no data found, return "No Flights Available"
    if not flights:
        return jsonify({
            "status_code": 404,
            "status": "Not Found",
            "message": "No Flights Available",
            "timestamp": datetime.now(),
            "data": []
        }), 200

    # Construct response
    column_names = [i[0] for i in cursor.description]
    formatted_data = [dict(zip(column_names, row)) for row in flights]
    cursor.close()

    return jsonify({
        "status_code": 200,
        "status": "success",
        "message": "Data retrieved successfully",
        "timestamp": datetime.now(),
        "data": formatted_data
    }), 200





#API DEPT DEST DATE
@app.route('/flights/from/<departure>/to/<destination>/on/<date>', methods=['GET'])
def get_flights_dept_dest_date(departure, destination, date):
    cursor = mysql.connection.cursor()    

    # Check if the departure is a country name
    cursor.execute('''
        SELECT Tiket_Penerbangan.kode_penerbangan, Tiket_Penerbangan.kode_pesawat, Tiket_Penerbangan.kode_maskapai, Tiket_Penerbangan.jumlah_tiket, Tiket_Penerbangan.dept_IATA, Tiket_Penerbangan.dest_IATA, Tiket_Penerbangan.dept_time, Tiket_Penerbangan.arriv_time, 
                   Tiket_Penerbangan.harga,departure_airport.nama_bandara AS departure_airport, 
                   departure_airport.nama_kota AS departure_city, 
                   departure_airport.nama_negara AS departure_country, 
                   arrival_airport.nama_bandara AS arrival_airport, 
                   arrival_airport.nama_kota AS arrival_city, 
                   arrival_airport.nama_negara AS arrival_country, 
                   Maskapai.nama_maskapai,
                   Pesawat.max_luggage
        FROM Tiket_Penerbangan
        INNER JOIN Bandara AS departure_airport ON Tiket_Penerbangan.dept_IATA = departure_airport.IATA
        INNER JOIN Bandara AS arrival_airport ON Tiket_Penerbangan.dest_IATA = arrival_airport.IATA
        INNER JOIN Maskapai ON Maskapai.kode_maskapai = Tiket_Penerbangan.kode_maskapai
        INNER JOIN Pesawat ON Pesawat.kode_pesawat = Tiket_Penerbangan.kode_pesawat
        WHERE (departure_airport.nama_negara = %s OR departure_airport.nama_kota = %s) AND (arrival_airport.nama_negara = %s OR arrival_airport.nama_kota = %s) AND DATE(Tiket_Penerbangan.dept_time) = %s;''', (departure, departure, destination, destination, date))
    flights = cursor.fetchall()

    # If no data found, return "No Flights Available"
    if not flights:
        return jsonify({
            "status_code": 404,
            "status": "Not Found",
            "message": "No Flights Available",
            "timestamp": datetime.now(),
            "data": []
        }), 200

    # Construct response
    column_names = [i[0] for i in cursor.description]
    formatted_data = [dict(zip(column_names, row)) for row in flights]
    cursor.close()

    return jsonify({
        "status_code": 200,
        "status": "success",
        "message": "Data retrieved successfully",
        "timestamp": datetime.now(),
        "data": formatted_data
    }), 200
#END OF API DEPT DEST DATE





#API DEPT DEST
@app.route('/flights/from/<departure>/to/<destination>', methods=['GET'])
def get_flights_dept_dest(departure, destination):
    cursor = mysql.connection.cursor()    

    # Check if the departure is a country name
    cursor.execute('''
        SELECT Tiket_Penerbangan.kode_penerbangan, Tiket_Penerbangan.kode_pesawat, Tiket_Penerbangan.kode_maskapai, Tiket_Penerbangan.jumlah_tiket, Tiket_Penerbangan.dept_IATA, Tiket_Penerbangan.dest_IATA, Tiket_Penerbangan.dept_time, Tiket_Penerbangan.arriv_time, 
                   Tiket_Penerbangan.harga,departure_airport.nama_bandara AS departure_airport, 
                   departure_airport.nama_kota AS departure_city, 
                   departure_airport.nama_negara AS departure_country, 
                   arrival_airport.nama_bandara AS arrival_airport, 
                   arrival_airport.nama_kota AS arrival_city, 
                   arrival_airport.nama_negara AS arrival_country, 
                   Maskapai.nama_maskapai,
                   Pesawat.max_luggage
        FROM Tiket_Penerbangan
        INNER JOIN Bandara AS departure_airport ON Tiket_Penerbangan.dept_IATA = departure_airport.IATA
        INNER JOIN Bandara AS arrival_airport ON Tiket_Penerbangan.dest_IATA = arrival_airport.IATA
        INNER JOIN Maskapai ON Maskapai.kode_maskapai = Tiket_Penerbangan.kode_maskapai
        INNER JOIN Pesawat ON Pesawat.kode_pesawat = Tiket_Penerbangan.kode_pesawat
        WHERE (departure_airport.nama_negara = %s OR departure_airport.nama_kota = %s) AND (arrival_airport.nama_negara = %s OR arrival_airport.nama_kota = %s)''', (departure, departure, destination, destination))
    flights = cursor.fetchall()

    # If no data found, return "No Flights Available"
    if not flights:
        return jsonify({
            "status_code": 404,
            "status": "Not Found",
            "message": "No Flights Available",
            "timestamp": datetime.now(),
            "data": []
        }), 200

    # Construct response
    column_names = [i[0] for i in cursor.description]
    formatted_data = [dict(zip(column_names, row)) for row in flights]
    cursor.close()

    return jsonify({
        "status_code": 200,
        "status": "success",
        "message": "Data retrieved successfully",
        "timestamp": datetime.now(),
        "data": formatted_data
    }), 200
#END OF API DEPT DEST





#API DEPT DATE
@app.route('/flights/from/<departure>/on/<date>', methods=['GET'])
def get_flights_dept_date(departure, date):
    cursor = mysql.connection.cursor()    

    # Check if the departure is a country name
    cursor.execute('''
        SELECT Tiket_Penerbangan.kode_penerbangan, Tiket_Penerbangan.kode_pesawat, Tiket_Penerbangan.kode_maskapai, Tiket_Penerbangan.jumlah_tiket, Tiket_Penerbangan.dept_IATA, Tiket_Penerbangan.dest_IATA, Tiket_Penerbangan.dept_time, Tiket_Penerbangan.arriv_time, 
                   Tiket_Penerbangan.harga,departure_airport.nama_bandara AS departure_airport, 
                   departure_airport.nama_kota AS departure_city, 
                   departure_airport.nama_negara AS departure_country, 
                   arrival_airport.nama_bandara AS arrival_airport, 
                   arrival_airport.nama_kota AS arrival_city, 
                   arrival_airport.nama_negara AS arrival_country, 
                   Maskapai.nama_maskapai,
                   Pesawat.max_luggage
        FROM Tiket_Penerbangan
        INNER JOIN Bandara AS departure_airport ON Tiket_Penerbangan.dept_IATA = departure_airport.IATA
        INNER JOIN Bandara AS arrival_airport ON Tiket_Penerbangan.dest_IATA = arrival_airport.IATA
        INNER JOIN Maskapai ON Maskapai.kode_maskapai = Tiket_Penerbangan.kode_maskapai
        INNER JOIN Pesawat ON Pesawat.kode_pesawat = Tiket_Penerbangan.kode_pesawat
        WHERE (departure_airport.nama_negara = %s OR departure_airport.nama_kota = %s) AND DATE(Tiket_Penerbangan.dept_time) = %s;''', (departure, departure, date))
    flights = cursor.fetchall()

    # If no data found, return "No Flights Available"
    if not flights:
        return jsonify({
            "status_code": 404,
            "status": "Not Found",
            "message": "No Flights Available",
            "timestamp": datetime.now(),
            "data": []
        }), 200

    # Construct response
    column_names = [i[0] for i in cursor.description]
    formatted_data = [dict(zip(column_names, row)) for row in flights]
    cursor.close()

    return jsonify({
        "status_code": 200,
        "status": "success",
        "message": "Data retrieved successfully",
        "timestamp": datetime.now(),
        "data": formatted_data
    }), 200
#END OF API DEPT DATE


#API DEPT
@app.route('/flights/from/<departure>', methods=['GET'])
def get_flights_dept(departure):
    cursor = mysql.connection.cursor()    

    # Check if the departure is a country name
    cursor.execute('''
       SELECT Tiket_Penerbangan.kode_penerbangan, Tiket_Penerbangan.kode_pesawat, Tiket_Penerbangan.kode_maskapai, Tiket_Penerbangan.jumlah_tiket, Tiket_Penerbangan.dept_IATA, Tiket_Penerbangan.dest_IATA, Tiket_Penerbangan.dept_time, Tiket_Penerbangan.arriv_time, 
                   Tiket_Penerbangan.harga,departure_airport.nama_bandara AS departure_airport, 
                   departure_airport.nama_kota AS departure_city, 
                   departure_airport.nama_negara AS departure_country, 
                   arrival_airport.nama_bandara AS arrival_airport, 
                   arrival_airport.nama_kota AS arrival_city, 
                   arrival_airport.nama_negara AS arrival_country, 
                   Maskapai.nama_maskapai,
                   Pesawat.max_luggage
        FROM Tiket_Penerbangan
        INNER JOIN Bandara AS departure_airport ON Tiket_Penerbangan.dept_IATA = departure_airport.IATA
        INNER JOIN Bandara AS arrival_airport ON Tiket_Penerbangan.dest_IATA = arrival_airport.IATA
        INNER JOIN Maskapai ON Maskapai.kode_maskapai = Tiket_Penerbangan.kode_maskapai
        INNER JOIN Pesawat ON Pesawat.kode_pesawat = Tiket_Penerbangan.kode_pesawat
        WHERE (departure_airport.nama_negara = %s OR departure_airport.nama_kota = %s)''', (departure, departure))
    flights = cursor.fetchall()

    # If no data found, return "No Flights Available"
    if not flights:
        return jsonify({
            "status_code": 404,
            "status": "Not Found",
            "message": "No Flights Available",
            "timestamp": datetime.now(),
            "data": []
        }), 200

    # Construct response
    column_names = [i[0] for i in cursor.description]
    formatted_data = [dict(zip(column_names, row)) for row in flights]
    cursor.close()

    return jsonify({
        "status_code": 200,
        "status": "success",
        "message": "Data retrieved successfully",
        "timestamp": datetime.now(),
        "data": formatted_data
    }), 200
#END OF API DEPT





#API DEST DATE
@app.route('/flights/to/<destination>/on/<date>', methods=['GET'])
def get_flights_dest_date(destination, date):
    cursor = mysql.connection.cursor()    

    # Check if the departure is a country name
    cursor.execute('''
        SELECT Tiket_Penerbangan.kode_penerbangan, Tiket_Penerbangan.kode_pesawat, Tiket_Penerbangan.kode_maskapai, Tiket_Penerbangan.jumlah_tiket, Tiket_Penerbangan.dept_IATA, Tiket_Penerbangan.dest_IATA, Tiket_Penerbangan.dept_time, Tiket_Penerbangan.arriv_time, 
                   Tiket_Penerbangan.harga,departure_airport.nama_bandara AS departure_airport, 
                   departure_airport.nama_kota AS departure_city, 
                   departure_airport.nama_negara AS departure_country, 
                   arrival_airport.nama_bandara AS arrival_airport, 
                   arrival_airport.nama_kota AS arrival_city, 
                   arrival_airport.nama_negara AS arrival_country, 
                   Maskapai.nama_maskapai,
                   Pesawat.max_luggage
        FROM Tiket_Penerbangan
        INNER JOIN Bandara AS departure_airport ON Tiket_Penerbangan.dept_IATA = departure_airport.IATA
        INNER JOIN Bandara AS arrival_airport ON Tiket_Penerbangan.dest_IATA = arrival_airport.IATA
        INNER JOIN Maskapai ON Maskapai.kode_maskapai = Tiket_Penerbangan.kode_maskapai
        INNER JOIN Pesawat ON Pesawat.kode_pesawat = Tiket_Penerbangan.kode_pesawat
        WHERE (arrival_airport.nama_negara = %s OR arrival_airport.nama_kota = %s) AND DATE(Tiket_Penerbangan.dept_time) = %s;''', (destination, destination, date))
    flights = cursor.fetchall()

    # If no data found, return "No Flights Available"
    if not flights:
        return jsonify({
            "status_code": 404,
            "status": "Not Found",
            "message": "No Flights Available",
            "timestamp": datetime.now(),
            "data": []
        }), 200

    # Construct response
    column_names = [i[0] for i in cursor.description]
    formatted_data = [dict(zip(column_names, row)) for row in flights]
    cursor.close()

    return jsonify({
        "status_code": 200,
        "status": "success",
        "message": "Data retrieved successfully",
        "timestamp": datetime.now(),
        "data": formatted_data
    }), 200
#END OF API DEST DATE





#API DEST
@app.route('/flights/to/<destination>', methods=['GET'])
def get_flights_dest(destination):
    cursor = mysql.connection.cursor()    

    # Check if the departure is a country name
    cursor.execute('''
       SELECT Tiket_Penerbangan.kode_penerbangan, Tiket_Penerbangan.kode_pesawat, Tiket_Penerbangan.kode_maskapai, Tiket_Penerbangan.jumlah_tiket, Tiket_Penerbangan.dept_IATA, Tiket_Penerbangan.dest_IATA, Tiket_Penerbangan.dept_time, Tiket_Penerbangan.arriv_time, 
                   Tiket_Penerbangan.harga,departure_airport.nama_bandara AS departure_airport, 
                   departure_airport.nama_kota AS departure_city, 
                   departure_airport.nama_negara AS departure_country, 
                   arrival_airport.nama_bandara AS arrival_airport, 
                   arrival_airport.nama_kota AS arrival_city, 
                   arrival_airport.nama_negara AS arrival_country, 
                   Maskapai.nama_maskapai,
                   Pesawat.max_luggage
        FROM Tiket_Penerbangan
        INNER JOIN Bandara AS departure_airport ON Tiket_Penerbangan.dept_IATA = departure_airport.IATA
        INNER JOIN Bandara AS arrival_airport ON Tiket_Penerbangan.dest_IATA = arrival_airport.IATA
        INNER JOIN Maskapai ON Maskapai.kode_maskapai = Tiket_Penerbangan.kode_maskapai
        INNER JOIN Pesawat ON Pesawat.kode_pesawat = Tiket_Penerbangan.kode_pesawat
        WHERE (arrival_airport.nama_negara = %s OR arrival_airport.nama_kota = %s)''', (destination, destination))
    flights = cursor.fetchall()

    # If no data found, return "No Flights Available"
    if not flights:
        return jsonify({
            "status_code": 404,
            "status": "Not Found",
            "message": "No Flights Available",
            "timestamp": datetime.now(),
            "data": []
        }), 200

    # Construct response
    column_names = [i[0] for i in cursor.description]
    formatted_data = [dict(zip(column_names, row)) for row in flights]
    cursor.close()

    return jsonify({
        "status_code": 200,
        "status": "success",
        "message": "Data retrieved successfully",
        "timestamp": datetime.now(),
        "data": formatted_data
    }), 200
#END OF API DEST





#API DATE
@app.route('/flights/on/<date>', methods=['GET'])
def get_flights_date(date):
    cursor = mysql.connection.cursor()    

    # Check if the departure is a country name
    cursor.execute('''
        SELECT Tiket_Penerbangan.kode_penerbangan, Tiket_Penerbangan.kode_pesawat, Tiket_Penerbangan.kode_maskapai, Tiket_Penerbangan.jumlah_tiket, Tiket_Penerbangan.dept_IATA, Tiket_Penerbangan.dest_IATA, Tiket_Penerbangan.dept_time, Tiket_Penerbangan.arriv_time, 
                   Tiket_Penerbangan.harga,departure_airport.nama_bandara AS departure_airport, 
                   departure_airport.nama_kota AS departure_city, 
                   departure_airport.nama_negara AS departure_country, 
                   arrival_airport.nama_bandara AS arrival_airport, 
                   arrival_airport.nama_kota AS arrival_city, 
                   arrival_airport.nama_negara AS arrival_country, 
                   Maskapai.nama_maskapai,
                   Pesawat.max_luggage
        FROM Tiket_Penerbangan
        INNER JOIN Bandara AS departure_airport ON Tiket_Penerbangan.dept_IATA = departure_airport.IATA
        INNER JOIN Bandara AS arrival_airport ON Tiket_Penerbangan.dest_IATA = arrival_airport.IATA
        INNER JOIN Maskapai ON Maskapai.kode_maskapai = Tiket_Penerbangan.kode_maskapai
        INNER JOIN Pesawat ON Pesawat.kode_pesawat = Tiket_Penerbangan.kode_pesawat
        WHERE DATE(Tiket_Penerbangan.dept_time) = %s;''', (date))
    flights = cursor.fetchall()

    # If no data found, return "No Flights Available"
    if not flights:
        return jsonify({
            "status_code": 404,
            "status": "Not Found",
            "message": "No Flights Available",
            "timestamp": datetime.now(),
            "data": []
        }), 200

    # Construct response
    column_names = [i[0] for i in cursor.description]
    formatted_data = [dict(zip(column_names, row)) for row in flights]
    cursor.close()

    return jsonify({
        "status_code": 200,
        "status": "success",
        "message": "Data retrieved successfully",
        "timestamp": datetime.now(),
        "data": formatted_data
    }), 200
#END OF API DATE






@app.route('/tickets/<kode_penerbangan>', methods=['GET'])
def get_ticket_detail(kode_penerbangan):
    
    def get_ticket_detail_from_database(kode_penerbangan):
        cursor = mysql.connection.cursor()
        cursor.execute('''
            SELECT * FROM Tiket_Penerbangan WHERE kode_penerbangan = %s
        ''', (kode_penerbangan,))
        ticket_detail = cursor.fetchone()
        cursor.close()
        return ticket_detail
    
    ticket_detail = get_ticket_detail_from_database(kode_penerbangan)
    if ticket_detail:
        return jsonify({
            "status_code": 200,
            "status": "success",
            "message": "Ticket detail retrieved successfully",
            "timestamp": datetime.now(),
            "data": ticket_detail
        }), 200
    else:
        return jsonify({
            "status_code": 404,
            "status": "Not Found",
            "message": "Ticket not found",
            "timestamp": datetime.now(),
            "data": {}
        }), 404







@app.route('/bookings', methods=['POST'])
def book_ticket():
    ticket_data = request.json

    if not ticket_data or 'kode_penerbangan' not in ticket_data or 'jumlah_tiket' not in ticket_data:
        return jsonify({
            "status_code": 400,
            "status": "Bad Request",
            "message": "Invalid ticket data",
            "timestamp": datetime.now(),
            "data": {}
        }), 400

    total_price = ticket_data.get('total_price')

    try:
        with mysql.connection.cursor() as cursor:
            cursor.execute('''
                INSERT INTO tabel_pemesanan (kode_penerbangan, jumlah_tiket, total_harga) 
                VALUES (%s, %s, %s)
            ''', (ticket_data['kode_penerbangan'], ticket_data['jumlah_tiket'], total_price))
            mysql.connection.commit()
        return jsonify({
            "status_code": 200,
            "status": "success",
            "message": "Ticket booked successfully",
            "timestamp": datetime.now(),
            "data": ticket_data
        }), 200
    except Exception as e:
        mysql.connection.rollback()
        print("Error booking ticket:", e)
        return jsonify({
            "status_code": 500,
            "status": "Internal Server Error",
            "message": "Failed to book ticket",
            "timestamp": datetime.now(),
            "data": {}
        }), 500




# second endpoint
## Show Detail Penerbangan
@app.route('/flights/<kode_penerbangan>', methods=['GET'])
def get_detail_penerbangan(kode_penerbangan):
    cursor = mysql.connection.cursor()    

    cursor.execute('''
        SELECT Tiket_Penerbangan.kode_penerbangan, Tiket_Penerbangan.kode_pesawat, Tiket_Penerbangan.kode_maskapai, Tiket_Penerbangan.jumlah_tiket, Tiket_Penerbangan.dept_IATA, Tiket_Penerbangan.dest_IATA, Tiket_Penerbangan.dept_time, Tiket_Penerbangan.arriv_time, 
                   Tiket_Penerbangan.harga,departure_airport.nama_bandara AS departure_airport, 
                   departure_airport.nama_kota AS departure_city, 
                   departure_airport.nama_negara AS departure_country, 
                   arrival_airport.nama_bandara AS arrival_airport, 
                   arrival_airport.nama_kota AS arrival_city, 
                   arrival_airport.nama_negara AS arrival_country, 
                   Maskapai.nama_maskapai,
                   Pesawat.max_luggage
        FROM Tiket_Penerbangan
        INNER JOIN Bandara AS departure_airport ON Tiket_Penerbangan.dept_IATA = departure_airport.IATA
        INNER JOIN Bandara AS arrival_airport ON Tiket_Penerbangan.dest_IATA = arrival_airport.IATA
        INNER JOIN Maskapai ON Maskapai.kode_maskapai = Tiket_Penerbangan.kode_maskapai
        INNER JOIN Pesawat ON Pesawat.kode_pesawat = Tiket_Penerbangan.kode_pesawat
        WHERE Tiket_Penerbangan.kode_penerbangan = %s
    ''', (kode_penerbangan,))
    penerbangan = cursor.fetchall()

    # Construct response
    column_names = [i[0] for i in cursor.description]
    formatted_data = [dict(zip(column_names, row)) for row in penerbangan]
    cursor.close()

    return jsonify({
        "status_code": 200,
        "status": "success",
        "message": "Data retrieved successfully",
        "timestamp": datetime.now(),
        "data": formatted_data
    }), 200




# third endpoint
### TAMBAH PENERBANGAN -- POST method --
@app.route('/addToPemesanan', methods=['POST'])
def add_flight():
    data = request.json
    cursor = mysql.connection.cursor()

    # Generate a unique identifier for kode_pemesanan
    unique_id = str(uuid.uuid4())  # Generate a UUID
    hash_object = hashlib.sha1(unique_id.encode())  # Create a SHA-1 hash object
    kode_pemesanan = hash_object.hexdigest()[:5]  # Extract the first 5 characters of the hash

    query = '''INSERT INTO Pemesanan (kode_pemesanan, kode_penerbangan, jumlah_tiket, total_harga)
               VALUES (%s, %s, %s, %s)
            '''
    values = (kode_pemesanan, data['kode_penerbangan'], data['jumlah_tiket'], data['total_harga'])
    cursor.execute(query, values)
    mysql.connection.commit()
    cursor.close()
    
    return jsonify({
        "status_code": 201,
        "status": "add success",
        "message": "Flight booked successfully",
        "kode_pemesanan": kode_pemesanan,
        "timestamp": datetime.now()
    }), 201













# third endpoint
### EDIT PENERBANGAN -- PUT method --
@app.route('/updateFlights/<int:flight_id>', methods=['PUT'])
def update_flight(flight_id):
    data = request.json
    cursor = mysql.connection.cursor()
    query = '''UPDATE flights
            SET flight_number = %s, airline_id = %s, departure_airport_code = %s, arrival_airport_code = %s, departure_time = %s, arrival_time = %s, fare = %s
            WHERE flight_id = %s
            '''
    values = (data['flight_number'], data['airline_id'], data['departure_airport_code'], data['arrival_airport_code'], data['departure_time'], data['arrival_time'], data['fare'], flight_id)
    cursor.execute(query, values)
    mysql.connection.commit()
    cursor.close()
    return jsonify({"status_code": "200","status": "success", "message": "Flight updated successfully", "timestamp": datetime.now()}), 200



# fourth endpoint
### HAPUS PENERBANGAN -- DELETE method --
@app.route('/deleteFlights/<identifier>', methods=['DELETE'])
def delete_flight(identifier):
    cursor = mysql.connection.cursor()
    if identifier.isdigit():
        flight_id = int(identifier)
        cursor.execute('DELETE FROM flights WHERE flight_id = %s', (flight_id,))
    else:
        arrival_country = identifier
        cursor.execute('''DELETE FROM flights WHERE arrival_airport_code 
                        IN 
                        (SELECT airport_code FROM airports WHERE country = %s)''', (arrival_country,))
    
    mysql.connection.commit()
    cursor.close()
    return jsonify({"status_code": "200","status": "success", "message": "Flight(s) deleted successfully", "timestamp": datetime.now()}), 200




# fifth endpoint
### TAMBAH DATA BANDARA -- POST method --
@app.route('/addairports', methods=['POST'])
def add_airport():
    data = request.json
    airport_code = data.get('airport_code')
    airport_name = data.get('airport_name')
    city = data.get('city')
    country = data.get('country')

    if not airport_code or not airport_name or not city or not country:
        return jsonify({"status_code": "400","status": "error", "message": "Data is incomplete", "timestamp": datetime.now()}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO airports (airport_code, airport_name, city, country) VALUES (%s, %s, %s, %s)", (airport_code, airport_name, city, country))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"status_code": "201","status": "add success", "message": "Airport data added successfully", "timestamp": datetime.now()}), 201




if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000)