
from src.services.mysql_connection import MySQLConnection
db = MySQLConnection.get_db()


class VechileFuelRelationship(db.Model):
    __tablename__="vechiles_fuels"
    id = db.Column(db.Integer, primary_key=True)
    vechile_id = db.Column(db.Integer, db.ForeignKey('vechile_segments.id', ondelete='CASCADE'), unique=False, nullable=False)
    fuel_id = db.Column(db.Integer, db.ForeignKey('fuels.id', ondelete='CASCADE'), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, unique=False, nullable=False)
    updated_at = db.Column(db.DateTime, unique=False, nullable=False)
    