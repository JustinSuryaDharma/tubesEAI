from datetime import datetime
from flask import Flask, jsonify, request, render_template, url_for
import requests
import os

app = Flask(__name__)

# get attractions
def filtered_attr(city):
  response_attraction = requests.get(f'http://localhost:3000/filterattractions?location={city}')
  return response_attraction.json()

# get article
def filtered_article(city):
  response_article = requests.get(f'http://127.0.0.1:5000/filterart?location={city}')
  return response_article.json()

# get city information
def city_info(city):
  response_city = requests.get(f'https://nominatim.openstreetmap.org/search?q={city}&format=json')
  return response_city.json()

# chat gpt interaction (for tourism info)
def input_user(user_input):
    url = "https://chatgpt-42.p.rapidapi.com/conversationgpt4"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "de85987dc7msha94ae4463722f1ep1b6118jsn8fa2737f13af",
        "X-RapidAPI-Host": "chatgpt-42.p.rapidapi.com",
    }

    payload = {
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ],
        "system_prompt": "",
        "temperature": 0.9,
        "top_k": 5,
        "top_p": 0.9,
        "max_tokens": 256,
        "web_access": False
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        output = result['result']
        return output
    except requests.exceptions.RequestException as e:
        print(f"Error making GPT request: {e}")
        return "An error occurred while processing your request. Please try again later."

# app routes
@app.route('/tourism')
def get_attraction():
    city = request.args.get('location')
    if city:
        attraction_info = filtered_attr(city)
        article_info = filtered_article(city)
        combined_info = {
          "attraction": attraction_info,
          "articles": article_info
        }
        user_image = url_for('static', filename='blog_image.jpg')
        return render_template('article.html', data_city=combined_info, user_image = user_image)
    else:
        return jsonify({'error': 'Location parameter is required'}), 400

@app.route('/submit', methods=['POST'])
def search():
        destination = str(request.form['destination'])
        url = "http://localhost:5000/flights/to/{}".format(destination)
        headers = {
            "Authorization": "justin",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            flight=response.json()
            flight=flight['data']
            return render_template('article.html', data=flight, datetime=datetime)
            # Do something with the data
        else:
            print("Error:", response.status_code) 

@app.route('/details')
def get_details():
    return render_template('details.html')

@app.route('/city')
def get_city():
  city = request.args.get('q')
  city_information = city_info(city)
  return jsonify(city_information)

# @app.route('/all_cities')
# def get_all():
#     return render_template('index.html', city=get_city, attraction=get_attraction)

@app.route('/gpt4', methods=['POST'])
def gpt4_interaction():
    data = request.get_json()
    user_input = data.get('user_input')

    if not user_input:
        return jsonify({'error': 'User input is required'}), 400

    response = input_user(user_input)
    return jsonify({'response': response})

if __name__ =="__main__":
  app.run(debug=True, port=5009)