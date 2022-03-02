from src.services.mysql_connection import MySQLConnection
db = MySQLConnection.get_db()


class Customers(db.Model):
    __tablename__="customers"
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.Enum('Male', 'Female', 'Transgender'), unique=False, nullable=False)
    customer_region = db.Column(db.Enum('East', 'West', 'North', 'South'), unique=False, nullable=False)
    income_group_id = db.Column(db.Integer, db.ForeignKey('income_group.id', ondelete='CASCADE'), unique=False, nullable=False)
    vechile_segment_id = db.Column(db.Integer, db.ForeignKey('vechile_segments.id', ondelete='CASCADE'), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, unique=False, nullable=False)
    updated_at = db.Column(db.DateTime, unique=False, nullable=False)
    income = db.relationship('IncomeGroup',cascade="all,delete", backref='customers',lazy=True)
    policies = db.relationship('Policies', secondary='customer_policies', back_populates="customers")
    vechile_segments = db.relationship('VechileSegments',cascade="all,delete", backref='customers',lazy=True)
