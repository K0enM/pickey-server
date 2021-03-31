import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_object(os.getenv('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

class Hanger(db.Model):
  __tablename__ = 'hangers'

  id = db.Column(db.Integer, primary_key=True)
  weight = db.Column(db.Float)

  def __init__(self, weight):
    self.weight = weight

  def __repr__(self):
    return '<id {}>'.format(self.id)

class HangerSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Hanger
    inlcude_fk = True

hanger_schema = HangerSchema()
hangers_schema = HangerSchema(many=True)

@app.route('/')
def hello():
  return 'Hello World!'

@app.route('/api/hangers')
def all_hangers():
  result = Hanger.query.all()
  return { "data": hangers_schema.dump(result)}

@app.route('/api/hanger/<id>', methods=['GET', 'DELETE', 'PUT'])
def hanger_handler(id):
  if request.method == 'GET':  
    result = Hanger.query.get(id)
    return { "data": hanger_schema.dump(result)}
  elif request.method == 'DELETE':
    result = Hanger.query.get(id)
    db.session.delete(result)
    db.session.commit()
    return {
      "data": "success"
    }
  elif request.method == 'PUT':
    obj = Hanger.query.get(id)
    data = request.json
    obj.weight = data["weight"]
    db.session.commit()
    return hanger_schema.dump(obj)

@app.route("/api/hanger/new", methods=['POST'])
def new_hanger():
  data = request.json
  result = Hanger(data["weight"])
  db.session.add(result)
  db.session.commit()
  return hanger_schema.dump(result)


if __name__ == '__main__':
  app.run()