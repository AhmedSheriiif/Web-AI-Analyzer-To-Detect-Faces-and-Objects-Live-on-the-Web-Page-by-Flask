from sqlalchemy_utils import URLType
from . import db


class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fullname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=True)
    comm_phone = db.Column(db.String(10), nullable=True)  # True/False
    comm_sms = db.Column(db.String(10), nullable=True)  # True/False
    comm_email = db.Column(db.String(10), nullable=True)  # True/False

    def __init__(self, fullname, email, password, phone, comm_phone, comm_sms, comm_email):
        self.fullname = fullname
        self.email = email
        self.password = password
        self.phone = phone
        self.comm_phone = comm_phone
        self.comm_sms = comm_sms
        self.comm_email = comm_email


class Videos(db.Model):
    __tablename__ = 'Videos'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=False, nullable=True)
    model = db.Column(db.String(255), unique=False, nullable=True)

    def __init__(self, name, email, model):
        self.name = name
        self.email = email
        self.model = model


class Images(db.Model):
    __tablename__ = 'Images'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(255), unique=False, nullable=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    model = db.Column(db.String(255), unique=False, nullable=True)

    def __init__(self, email, img, name, mimetype, model):
        self.email = email
        self.name = name
        self.img = img
        self.mimetype = mimetype
        self.model = model


class Cameras(db.Model):
    __tablename__ = 'Cameras'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(255), unique=False, nullable=False)
    link = db.Column(db.String(255), unique=False, nullable=False)
    name = db.Column(db.String(255), unique=False, nullable=True)
    location = db.Column(db.String(255), unique=False, nullable=True)
    model = db.Column(db.String(255), unique=False, nullable=True)

    def __init__(self, email, link, location, model, name):
        self.email = email
        self.link = link
        self.type = type
        self.location = location
        self.model = model
        self.name = name


### EVENTS ###
class Events(db.Model):
    __tablename__ = 'Events'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(255), unique=False, nullable=False)
    model = db.Column(db.String(255), unique=False, nullable=False)
    source = db.Column(db.String(255), unique=False, nullable=True)  # Video, Image, Camera
    source_name = db.Column(db.String(255), unique=False, nullable=True)  # Name of the source (myimg.png)
    message = db.Column(db.String(255), unique=False, nullable=True)
    event_date = db.Column(db.DateTime)
    event_link = db.Column(URLType)

    def __init__(self, email: object, model: object, source: object, source_name: object, message: object,
                 event_date: object, event_link: object) -> object:
        self.email = email
        self.model = model
        self.source = source
        self.source_name = source_name
        self.message = message
        self.event_date = event_date
        self.event_link = event_link
