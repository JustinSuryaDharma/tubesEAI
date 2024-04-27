from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# get attractions
def filtered_attr(city):
  response_attraction = requests.get(f'http://localhost:3000/filterattractions?location={city}')
  return response_attraction.json()

# get article
def filtered_article(city):
  response_article = requests.get(f'http://127.0.0.1:5000/filterart?location={city}')
  return response_article.json()

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
        return jsonify(combined_info)
    else:
        return jsonify({'error': 'Location parameter is required'}), 400


if __name__ =="__main__":
  app.run(debug=True, port=5009)