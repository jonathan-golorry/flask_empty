from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import request
from geodata import get_geodata

db = SQLAlchemy()

class Request(db.Model):
    __tablename__ = 'empty_request'

    id = db.Column(db.Integer, primary_key=True)
    browser = db.Column(db.String)
    date = db.Column(db.DateTime)
    event = db.Column(db.String)
    url = db.Column(db.String)
    ip_address = db.Column(db.String)
    geolocation = db.Column(db.String)
    #site_id = db.Column(db.Integer, db.ForeignKey('tracking_site.id'))

    def __init__(self):
        self.browser = request.headers.get("User-Agent")
        self.date = datetime.utcnow()
        self.event = request.values.get("event")
        self.url = request.values.get("url") or request.headers.get("Referer")

        ip = request.access_route[0] or request.remote_addr
        self.ip_address = ip
        geodata = get_geodata(ip)
        self.geolocation = str(geodata.get("city"))
        #location = "{}, {}".format(geodata.get("city"),
        #                           geodata.get("zipcode"))



    def __repr__(self):
        return '<Visit %r - %r>' % (self.url, self.date)





