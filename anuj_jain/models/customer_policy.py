
from src.services.mysql_connection import MySQLConnection
db = MySQLConnection.get_db()


class CustomerPoliciesRelationship(db.Model):
    __tablename__="customer_policies"
    id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey('policies.id', ondelete='CASCADE'), unique=False, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='CASCADE'), unique=False, nullable=False)
    maritial_status = db.Column(db.Boolean, unique=False, nullable=False)
    created_at = db.Column(db.DateTime, unique=False, nullable=False)
    updated_at = db.Column(db.DateTime, unique=False, nullable=False)
    