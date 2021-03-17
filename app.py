import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__)
app.config.from_object(os.getenv('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Hanger(db.Model):
  __tablename__ = 'hangers'

  id = db.Column(db.Integer, primary_key=True)
  weight = db.Column(db.Float)

  def __init__(self, weight):
    self.weight = weight

  def __repr__(self):
    return '<id {}>'.format(self.id)

@app.route('/')
def hello():
  return 'Hello World!'

@app.route('/hangers')
def all_hangers():
  return jsonify(db.session.query(Hanger))

if __name__ == '__main__':
  app.run()