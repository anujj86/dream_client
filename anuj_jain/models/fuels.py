
from src.services.mysql_connection import MySQLConnection
db = MySQLConnection.get_db()


class Fuels(db.Model):
    __tablename__="fuels"
    id = db.Column(db.Integer, primary_key=True)
    fuel_type = db.Column(db.Enum('CNG', 'Petrol', 'Diesel'), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, unique=False, nullable=False)
    updated_at = db.Column(db.DateTime, unique=False, nullable=False)
    vechile_segments = db.relationship('VechileSegments', secondary='vechiles_fuels', back_populates="fuels")