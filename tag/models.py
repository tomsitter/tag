from sqlalchemy import Column, Integer, String
from tag import db

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)

class Image(db.Model):
    # __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    description = Column(String(500))
    filename = Column(String(50), unique=True)
    latitude = Column(String(12))
    longitude = Column(String(12))

    def __init__(self, title, description, filename, latitude, longitude):
        self.title = title
        self.description = description
        self.filename = filename
        self.latitude = latitude or None
        self.longitude = longitude or None

    def __repr__(self):
        return '<Image %r>' % self.title
