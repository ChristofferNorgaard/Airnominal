from os import stat
from flask import Blueprint, request, jsonify, make_response
from schema import Optional, Or, Schema, SchemaError
from ..database import Measurement, Station, Sensor, MeasurementType
from ..utils import returnError
from secrets import token_hex
from ..database import Session
from datetime import datetime
from dateutil import parser

class PlatformsHandler:
    def __init__(self):
        self.session =  Session()
        self.reg = Blueprint('platforms', __name__)
        self.registerRouts()
    def registerRouts(self):
        @self.reg.route("/", methods = ['GET'])
        def getStations():
            l = []
            for s in self.session.query(Station).all():
                a = {
                    "id" : str(s.id),
                    "name" : s.name,
                    "sensors" : []
                }
                for sen in s.sensors:
                    a["sensors"].append({
                        "name": sen.modelname,
                        "mes_type": sen.MeasurementType.name,
                        "unit": sen.MeasurementType.unit
                    })
                l.append(a)
            response = make_response(
                jsonify(l
                ),
                200,
            )
            return response
        @self.reg.route("/new", methods = ['POST'])
        def registerNewStation():
            schema = Schema({
                "name": str,
                "platform": str,
                "sensors": [
                    {
                        "name": str,
                        "mes_type": str,
                    }
                ],
            })
            try:
                con = schema.validate(request.json)
            except:
                return returnError("schema not validated")
            key = token_hex()
            station = Station(name = con["name"])
            station.set_password(key)
            s = []
            for i in con["sensors"]:
                m = self.session.query(MeasurementType).filter(MeasurementType.name == i["mes_type"]).all()
                if not m:
                    return returnError(i["mes_type"] + " measurement type does not exist")
                m = m[0]
                sensor = Sensor(modelname = i["name"])
                s.append(sensor)
                station.sensors.append(sensor)
            m.sensors.extend(s)
            self.session.add(station)
            for i in s:
                self.session.add(i)
            self.session.commit()
            response = make_response(
                jsonify(
                    {
                        "success": True,
                        "id": str(station.id),
                        "key": key,
                        "sensors" : [{"name": i.modelname, "id": i.id} for i in s]
                    }
                ),
                200,
            )
            response.headers["Content-Type"] = "application/json"
            return response
        @self.reg.route("/new/type", methods = ['POST'])
        def newMeasurementType():
            schema = Schema({
                "name": str,
                "unit": str
            })
            try:
                con = schema.validate(request.json)
            except:
                return returnError("schema not validated")
            m = self.session.query(MeasurementType).filter(MeasurementType.name == con["name"]).all()
            print(m)
            if m:
                return returnError("already exists")
            m = MeasurementType(name=con["name"], unit=con["unit"])
            self.session.add(m)
            response = make_response(
                jsonify(
                    {
                        "success": True,
                    }
                ),
                200,
            )
            response.headers["Content-Type"] = "application/json"
            return response
        @self.reg.route("/new/mes", methods = ['POST'])
        def submitMeasurements():
            schema = Schema([{
                "id": str,
                "key": str,
                "sen": [
                    {
                        "sen_id": str,
                        "mes": [
                            {
                                "value": float,
                                "lon": float,
                                "lat": float,
                                Optional("isoTime") : str
                            }
                        ],
                    }
                ],
            }])
            try:
                con = schema.validate(request.json)
            except:
               return returnError("First schema not validated")
            for stat in con:
                s = self.session.query(Station).filter(Station.id == int(stat["id"])).all()
                if not s:
                    return returnError("Station id " + stat["id"] + " does not exist")
                s = s[0]
                if not s.is_correct_password(stat["key"]):
                    return returnError("Wrong password")
                for sen in stat["sen"]:
                    se = self.session.query(Sensor).filter(Sensor.id == int(sen["sen_id"])).all()
                    if not sen:
                        return returnError("Sensor id " + sen["sen_id"] + " does not exist")
                    se = se[0]
                    for mes in sen["mes"]:
                        time = None
                        if "isoTime" in mes.keys():
                            try:
                                time = parser.parse(mes["isoTime"])
                            except:
                                return returnError(mes["isoTime"] + " is not valid iso format timestamp")
                        else:
                            time = datetime.now()
                        m = Measurement(value = mes["value"], datetime=time, lon=mes["lon"], lat=mes["lat"])
                        self.session.add(m)
                        se.measurements.append(m)
            response = make_response(
                jsonify(
                    {
                        "success": True,
                    }
                ),
                200,
            )
            self.session.commit()
            response.headers["Content-Type"] = "application/json"
            return response

                
    


            
            
            

                


    
