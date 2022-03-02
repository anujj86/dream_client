from src.services.mysql_connection import MySQLConnection
db = MySQLConnection.get_db()


class IncomeGroup(db.Model):
    __tablename__="income_group"
    id = db.Column(db.Integer, primary_key=True)
    min_income = db.Column(db.Float, unique=False, nullable=False)
    max_income = db.Column(db.Float, unique=False, nullable=False)
    created_at = db.Column(db.DateTime, unique=False, nullable=False)
    updated_at = db.Column(db.DateTime, unique=False, nullable=False)