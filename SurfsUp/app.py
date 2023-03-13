import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine=create_engine(f"sqlite:///./Resources/hawaii.sqlite")
Base=automap_base()
Base.prepare(autoload_with=engine)

Measurement=Base.classes.measurement
Station=Base.classes.station

session=Session(engine)

app=Flask(__name__)

# 1.
@app.route ("/")
def welcome():
    
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"Temperature-Most Active Station(2016):<br/>"
        f"/api/v1.0/tobs<br/>"
        f"Temperature Stats 2010-2017(Enter Start Date):<br/>"
        f"/api/v1.0/<start>yyyy-mm-dd<br/>"
        f"Temperature Stats 2010-2017(Enter Date Range):<br/>"
        f"/api/v1.0/<start>yyyy-mm-dd/<end>yyyy-mm-dd"
    )

# 2.
@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation_data=session.query(Measurement.date, Measurement.prcp).\
                        filter(Measurement.date>=dt.datetime(2016, 8, 23)).all()
    
    precipitation_dict=list(np.ravel(precipitation_data))
    return jsonify(precipitation_dict)

# 3.
@app.route("/api/v1.0/stations")
def station():
    station_data=session.query(Measurement.station).group_by(Measurement.station).distinct().all()
    
    station_dict=list(np.ravel(station_data))
    return jsonify(station_dict)

# 4.
@app.route("/api/v1.0/tobs")
def temperature():
    temperature_data=session.query(Measurement.date, Measurement.tobs).\
                filter((Measurement.station)=="USC00519523").filter(func.strftime("%Y",Measurement.date) == "2016").all()
    
    temperature_dict=list(np.ravel(temperature_data))
    return jsonify(temperature_dict)

# 5.
@app.route("/api/v1.0/<start>")
def temp_start (start):
    start_date=dt.datetime.strptime(start,"%Y-%m-%d")
    sel= [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    temp_stats=session.query(*sel).filter(Measurement.date>=start_date).all()

    temp_stats_list = []
    for row in temp_stats:
        temp_stats_list.append({
            "TMIN": row[0],
            "TAVG": row[1],
            "TMAX": row[2]
        })
    return jsonify(temp_stats_list)

@app.route("/api/v1.0/<start>/<end>")
def temp_range(start,end):
    start_date1=dt.datetime.strptime(start,"%Y-%m-%d")
    end_date=dt.datetime.strptime(end,"%Y-%m-%d")
    sel= [func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]
    temp_stats1=session.query(*sel).filter(Measurement.date>=start_date1).filter(Measurement.date<=end_date).all()

    temp_stats_list1 = []
    for row in temp_stats1:
        temp_stats_list1.append({
            "TMIN": row[0],
            "TAVG": row[1],
            "TMAX": row[2]
        })
    return jsonify(temp_stats_list1)

session.close()

if __name__ == '__main__':
    app.run(debug=True)

