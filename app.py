import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurements
Stations = Base.classes.stations

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f" Search all temps from current to specified date.<br/>"
        f"/api/v1.0/YYYY-mm-dd<br/>"
        f"<br/>"
        f"Search a date range using the template below.<br/>"
        f"/api/v1.0/YYYY-mm-dd/YYYY-mm-dd<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Precipiation by date for 2017"""
    # Query prcp data for 2017
    results = session.query(Measurements.date, Measurements.prcp).\
    filter(func.strftime("%Y", Measurements.date) == "2017").all() 

    # Create a dictionary
    date = [result[0] for result in results[:-1]]
    prcp = [result[1] for result in results[:-1]]
    dic = dict(zip(date, prcp))

    return jsonify(dic)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Query all stations
    results = session.query(Stations.station, Stations.name).all()

     # Create a dictionary 
    station = [result[0] for result in results[:-1]]
    name = [result[1] for result in results[:-1]]
    dic = dict(zip(station, name))

    return jsonify(dic)

@app.route("/api/v1.0/tobs")
def tobs():
    """Tobs data by date for 2017"""
   # Query tobs data for 2017
    results = session.query(Measurements.date, Measurements.tobs).\
    filter(func.strftime("%Y", Measurements.date) == "2017").all() 

     # Create a dictionary 
    date = [result[0] for result in results[:-1]]
    tobs = [result[1] for result in results[:-1]]
    dic = dict(zip(date, tobs))

    return jsonify(dic)

@app.route("/api/v1.0/<start>")
def start(start):
    """Tmin Tmax and Tavg """
    # Query all dates greater than or equal to start date
    results = session.query(Measurements.tobs).\
    filter(Measurements.date >= start).all()

    # Create a dictionary 
    tobs = list(np.ravel(results))

    # Define Tmax, Tmin, Tavg
    tobs_max = np.max(tobs)
    tobs_min = np.min(tobs)
    tobs_mean = np.mean(tobs)

    dic = {"Max Temp": int(tobs_max), 
           "Min Temp": int(tobs_min), 
           "Avg Temp": int(tobs_mean)
          }
    return jsonify(dic)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Tmin Tmax and Tavg """
    # Query all dates greater than or equal to start date
    results = session.query(Measurements.tobs).\
    filter(Measurements.date >= start, Measurements.date >= end ).all()

    # Create a dictionary 
    tobs = list(np.ravel(results))

    # Define Tmax, Tmin, Tavg
    tobs_max = np.max(tobs)
    tobs_min = np.min(tobs)
    tobs_mean = np.mean(tobs)

    dic = {"Max Temp": int(tobs_max), 
           "Min Temp": int(tobs_min), 
           "Avg Temp": int(tobs_mean)
          }
    return jsonify(dic)



if __name__ == '__main__':
    app.run(debug=True)