# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 23:12:28 2021

@author: Viji
"""
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})


Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#weather app
app = Flask(__name__)


latestDate = (session.query(Measurement.date)
                .order_by(Measurement.date.desc())
                .first())
latestDate = list(np.ravel(latestDate))[0]

latestDate = dt.datetime.strptime(latestDate, '%Y-%m-%d')
latestYear = int(dt.datetime.strftime(latestDate, '%Y'))
latestMonth = int(dt.datetime.strftime(latestDate, '%m'))
latestDay = int(dt.datetime.strftime(latestDate, '%d'))

yearBefore = dt.date(latestYear, latestMonth, latestDay) - dt.timedelta(days=365)
yearBefore = dt.datetime.strftime(yearBefore, '%Y-%m-%d')




@app.route("/")
def home():
    return (f"Hawaii Climate_Surfs Up! <br/>"
            f"------------------------------<br/>"
            f"Available Routes:<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/precipitaton<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/datesearch/<startDate><br/>"
            f"/api/v1.0/datesearchRange/<startDate>/<endDate><br/>"
            f"---------------------------------------")


@app.route("/api/v1.0/precipitaton")
def precipitation():
    
    results = (session.query(Measurement.date, Measurement.prcp, Measurement.station)
                      .filter(Measurement.date > yearBefore)
                      .order_by(Measurement.date)
                      .all())
    
    precipData = []
    for result in results:
        precipDict = {result.date: result.prcp, "Station": result.station}
        precipData.append(precipDict)

    return jsonify(precipData)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.name).all()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    results = (session.query(Measurement.date,Measurement.station, Measurement.tobs)
               .filter(Measurement.date > yearBefore)
               .order_by(Measurement.date)
               .all())
    TobsData = []
    for result in results:
        TobsDict = {result.date: result.tobs, "Station": result.station}
        TobsData.append(TobsDict)

    return jsonify(TobsData)    

@app.route('/api/v1.0/datesearch/<startDate>')
def start(startDate):
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results =  (session.query(*sel)
                       .filter(func.strftime("%Y-%m-%d", Measurement.date) >= startDate)
                       .group_by(Measurement.date)
                       .all())

    dates = []                       
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["Low Temp"] = result[1]
        date_dict["Avg Temp"] = result[2]
        date_dict["High Temp"] = result[3]
        dates.append(date_dict)
    return jsonify(dates)

@app.route('/api/v1.0/datesearchRange/<startDate>/<endDate>')
def startEnd(startDate, endDate):
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results =  (session.query(*sel)
                       .filter(func.strftime("%Y-%m-%d", Measurement.date) >= startDate)
                       .filter(func.strftime("%Y-%m-%d", Measurement.date) <= endDate)
                       .group_by(Measurement.date)
                       .all())

    dates = []                       
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["Low Temp"] = result[1]
        date_dict["Avg Temp"] = result[2]
        date_dict["High Temp"] = result[3]
        dates.append(date_dict)
    return jsonify(dates)


if __name__ == "__main__":
    app.run(debug=True)
