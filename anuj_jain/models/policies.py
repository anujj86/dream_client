from enum import unique
from src.services.mysql_connection import MySQLConnection
db = MySQLConnection.get_db()


class Policies(db.Model):
    __tablename__="policies"
    id = db.Column(db.Integer, primary_key=True)
    dop = db.Column(db.DateTime, unique=False, nullable=False)
    premium = db.Column(db.Float, unique=False, nullable=False)
    body_injury_libality = db.Column(db.Boolean, unique=False, nullable=False)
    personal_injury_protection = db.Column(db.Boolean, unique=False, nullable=False)
    property_damage_libality = db.Column(db.Boolean, unique=False, nullable=False)
    collision = db.Column(db.Boolean, unique=False, nullable=False)
    comprehensive = db.Column(db.Boolean, unique=False, nullable=False)
    created_at = db.Column(db.DateTime, unique=False, nullable=False)
    updated_at = db.Column(db.DateTime, unique=False, nullable=False)
    customers = db.relationship('Customers', secondary='customer_policies', back_populates="policies")