# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 23:12:28 2021

@author: Viji
"""

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/huwaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/dates<br/>"
    )


@app.route("/api/v1.0/dates")
def dates():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger dates"""
    # Query all passengers
    results = session.query(meaurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_dates = list(np.ravel(results))

    return jsonify(all_dates)