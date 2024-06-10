from flask import Flask, jsonify, request
from kafka import KafkaProducer
from kafka.errors import KafkaError
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

# app 
app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init 
db = SQLAlchemy(app)
ma = Marshmallow(app)

# model
class Article(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(20), unique=True)
  content = db.Column(db.String(300))
  author = db.Column(db.String(20))
  date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
  
  def __init__(self, title, content, author):
    self.title = title
    self.content = content
    self.author = author
    
# schema 
class ArticleSchema(ma.Schema):
  class Meta:
    fields = ('id', 'title', 'content', 'author', 'date_created')
    
article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)

# route 
@app.route('/article', methods=['POST'])
def add_article():
    title = request.json['title']
    content = request.json['content']
    author = request.json['author']
    
    new_article = Article(title, content, author)
    
    db.session.add(new_article)
    db.session.commit()
    
    return article_schema.jsonify(new_article)
  
@app.route('/article', methods=['GET'])
def get_articles():
  all_article = Article.query.all()
  result = articles_schema.dump(all_article)
  return jsonify(result)

@app.route('/article/<id>', methods=['GET'])
def get_article(id):
  article = Article.query.get(id)
  return article_schema.jsonify(article)

@app.route('/article/<id>', methods=['PUT'])
def update_article(id):
  article = Article.query.get(id)
  
  title = request.json['title']
  content = request.json['content']
  author = request.json['author']
  
  article.title = title
  article.content = content
  article.author = author
  
  db.session.commit()
  
  return article_schema.jsonify(article)

@app.route('/article/<id>', methods=['DELETE'])
def del_article(id):
    article = Article.query.get(id)
    db.session.delete(article)
    db.session.commit()
    
    return article_schema.jsonify(article)
  
@app.route('/filterart', methods=['GET'])
def filtered_articles():
    city_name = request.args.get('location')

    if city_name:
        articles = Article.query.filter(
            (Article.title.like(f"%{city_name}%")) |
            (Article.content.like(f"%{city_name}%"))
        ).all()
    else:
        articles = Article.query.all()

    return article_schema.jsonify(articles, many=True)


# server
if __name__ == '__main__':
  app.run(debug=True, port=5500)