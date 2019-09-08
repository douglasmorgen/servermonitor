import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import render_template
import datetime
import os
from flask import json
from sqlalchemy.sql.functions import func
import threading
import time
import random

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(120))
    timestamp = db.Column(db.DateTime)

    def __init__(self, code, timestamp):
        
        self.code = code
        self.timestamp = timestamp

class ResponseSchema(ma.Schema):
    class Meta:
        fields = ('timestamp','code')

response_schema = ResponseSchema()
responses_schema = ResponseSchema(many=True)

@app.route("/show_responses", methods=["GET"])
def show_responses(minutes_searched=5):
    
    lower_time_limit=datetime.datetime.utcnow()+datetime.timedelta( minutes=-minutes_searched)

    all_responses = Response.query.filter(Response.timestamp>lower_time_limit).order_by(Response.timestamp.desc()).all()
    result = responses_schema.dump(all_responses)
    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return jsonify(isError= False,
                    message= "List of Responses",
                    statusCode= 200,
                    response= result), 200

    #return response

# # polling method
@app.route("/poll", methods=["GET"])
def add_report():
    
    new_response= poll()
    result = response_schema.dump(new_response)

    response = app.response_class(
    response=json.dumps(result),
    status=200,
    mimetype='application/json'
    )
    return jsonify(isError= False,
                    message= "Response Added",
                    statusCode= 200,
                    response= result), 200
    
    #return response

def poll():
    #handle non-response
    error=False
    try:
        f = requests.get("http://localhost:12345/",timeout=2)
    except requests.exceptions.RequestException as e:  
        error=True

    if error:
        code='non-response'
    else:
        code=str(f.status_code)

    timestamp =datetime.datetime.utcnow()
    new_response = Response(code, timestamp)
    
    db.session.add(new_response)
    db.session.commit()
    

    return new_response
    #return jsonify(f)
    #return True

@app.route("/frontend", methods=["GET"])
def frontend():
    #return last 10 polls, non-response/500/200 counts in last 5 minutes
    minutes_searched=5
    lower_time_limit=datetime.datetime.utcnow()+datetime.timedelta( seconds=-60*minutes_searched)
    responses=Response.query.filter(Response.timestamp>lower_time_limit).order_by(Response.timestamp.desc()).limit(10).all()
    

    rawcounts=db.session.query(Response.code, func.count(Response.id).label('count')).group_by(Response.code).filter(Response.timestamp>lower_time_limit).all()
    
    return render_template("frontend.html", responses=responses,rawcounts=rawcounts)

# TO DO: Create frontend api that returns just the data you need to update: last 10 responses and the counts of each response code
# @app.route("/frontendapi", methods=["GET"])
# def frontendapi():
#     #return last 10 polls, non-response/500/200 counts in last 5 minutes
#     minutes_searched=5
#     lower_time_limit=datetime.datetime.utcnow()+datetime.timedelta( seconds=-60*minutes_searched)
#     responses=Response.query.filter(Response.timestamp>lower_time_limit).order_by(Response.timestamp.desc()).limit(10).all()
#     rawcounts=db.session.query(Response.code, func.count(Response.id).label('count')).group_by(Response.code).filter(Response.timestamp>lower_time_limit).all()
#     json_response=json.dumps(responses)+json.dumps(rawcounts)
#     resp = Response(js, status=200, mimetype='application/json')
#     response = app.response_class(
#         response=json_response,
#         status=200,
#         mimetype='application/json'
#     )

#     return render_template("frontend.html", responses=responses,rawcounts=rawcounts)

def update(min_secs=5, max_secs=15, first_time=False):
    
    app.config['updated'] = not first_time
    delay = random.randint(min_secs, max_secs)
    threading.Timer(delay, update).start()
    poll()
    #delete every so often
    if random.randint(0, 10)==1:
        #delete all records older than 20 minutes
        delete_threshold_minutes=20
        lower_delete_threshold=datetime.datetime.utcnow()+datetime.timedelta( minutes=-delete_threshold_minutes)

        db.session.query(Response).filter(Response.timestamp<lower_delete_threshold).delete()
        db.session.commit()

update(first_time=True)

if __name__ == '__main__':
    app.run(debug=True)