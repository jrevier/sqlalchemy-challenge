import sqlalchemy
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


app = Flask(__name__)

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station




@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return( f"Available Routes: <br/>"
        f"Precipitation data for the last year : /api/v1.0/precipitation<br/>"
        f"Station List: /api/v1.0/stations<br/>"
        f"Temperature data for the last year: /api/v1.0/tobs<br/>"
        f"Enter a start date: /api/v1.0/<start><br/>"
        f"Enter a start and end date: /api/v1.0/<start>/<end><br/>"
          )
        
@app.route("/api/v1.0/precipitation")

def precipitation():

    session = Session(engine)

    results = session.query(Measurement.date, Measurement.station,Measurement.prcp).\
                        filter(Measurement.date >="2016-08-23").\
                        order_by(Measurement.date).all()

    session.close()

    precip = list(np.ravel(results))

    return jsonify(precip)

@app.route("/api/v1.0/stations")

def stations():
    session = Session(engine)
    
    query = session.query(Station.station, Station.name).all()
    
    session.close()
    
    stations = list(np.ravel(query))
    
    return jsonify(stations)

@app.route("/api/v1.0/tobs")

def tobs(): 
    
    session = Session(engine)
    
    tobs = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
                    filter(Measurement.date >="2016-08-23").\
                    order_by(Measurement.date).all()
    session.close()
    
    temp = list(np.ravel(tobs))
    
    return jsonify(temp)

@app.route("/api/v1.0/<start>")

def start(start): 
    session = Session(engine)
    start_stats = session.query\
    (func.min(Measurement.tobs).label('min'),\
    func.avg(Measurement.tobs).label('avg'),\
    func.max(Measurement.tobs).label('max')).\
    filter(Measurement.date >= start).all()
    

    start_stats_list = []
    for s in start_stats:
        start_stats_dict = {}
        start_stats_dict['Start Date'] = start
        start_stats_dict['Min Temp'] = s.min
        start_stats_dict['Avg Temp'] = s.avg
        start_stats_dict['Max Temp'] = s.max
        start_stats_list.append(start_stats_dict)
    
    return jsonify(start_stats_list)


@app.route("/api/v1.0/<start>/<end>")

def range_temps(start,end): 
    
    session = Session(engine)
    range_stats= session.query(func.min(Measurement.tobs).label('min'),\
    func.avg(Measurement.tobs).label('avg'),\
    func.max(Measurement.tobs).label('max')).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()

    range_stats_list = []
    for s in range_stats:
        range_dict = {}
        range_dict['Start Date'] = start
        range_dict['End Date'] = end
        range_dict['Min Temp'] = s.min
        range_dict['Avg Temp'] = s.avg
        range_dict['Max Temp'] = s.max
        range_stats_list.append(range_dict)
    
    return jsonify(range_stats_list)


if __name__ == '__main__':
    app.run(debug=True)
