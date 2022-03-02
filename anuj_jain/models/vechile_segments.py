from src.services.mysql_connection import MySQLConnection
db = MySQLConnection.get_db()


class VechileSegments(db.Model):
    __tablename__="vechile_segments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, unique=False, nullable=False)
    updated_at = db.Column(db.DateTime, unique=False, nullable=False)
    fuels = db.relationship('Fuels', secondary='vechiles_fuels', back_populates="vechile_segments")