import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    
    return (
        f"Welcome to my homepage!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")

def precipitation():

    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > '2016-08-24').\
        filter(Measurement.date <= '2017-08-23').\
        order_by(Measurement.date).\
        all()

    return jsonify(results)



@app.route("/api/v1.0/stations")

def stations():

    station = session.query(Station.station, Station.name).all()

    return jsonify(station)





@app.route("/api/v1.0/tobs")

def tobs():

    temp = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
    filter(Measurement.date > '2016-08-24').\
    filter(Measurement.date <= '2017-08-23').\
    all()

    return jsonify(temp)



@app.route("/api/v1.0/<start>")

def startDateOnly(start):

    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    return jsonify(result)





@app.route("/api/v1.0/<start>/<end>")

def startDateEndDate(start,end):

    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()

    return jsonify(result)



if __name__ == "__main__":
    app.run(debug=True)