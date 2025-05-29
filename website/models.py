from . import db
from flask_login import UserMixin
from datetime import datetime


# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=db.func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     def __repr__(self):
#         return f'<Note {self.id}>'
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    #notes = db.relationship('Note', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'
    
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<City {self.name}>'

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    to_city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    train_name = db.Column(db.String(100), nullable=False)
    departure = db.Column(db.Time, nullable=False)
    arrival = db.Column(db.Time, nullable=False)
    duration = db.Column(db.String(20), nullable=False)

    from_city = db.relationship('City', foreign_keys=[from_city_id], backref='departures')
    to_city = db.relationship('City', foreign_keys=[to_city_id], backref='arrivals')

    def __repr__(self):
        return f'<Route {self.from_city.name} -> {self.to_city.name}>'