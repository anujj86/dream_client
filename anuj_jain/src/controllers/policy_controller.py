from models.customers import Customers
from models.policies import Policies
from models.customer_policy import CustomerPoliciesRelationship
from sqlalchemy import or_
from sqlalchemy.sql.functions import func
from src.services.mysql_connection import MySQLConnection
from sqlalchemy import desc

db = MySQLConnection.get_db()

def get_all_policies(query, page_size, page_number):
    customer_policies = None
    if query is None:
        customer_policies = CustomerPoliciesRelationship.query.order_by(desc(CustomerPoliciesRelationship.id)).limit(page_size).offset(page_size*(page_number-1))
    else: 
        customer_policies = CustomerPoliciesRelationship.query.filter(\
            or_(CustomerPoliciesRelationship.policy_id.ilike(f'%%{query}%%'), \
            CustomerPoliciesRelationship.customer_id.ilike(f'%%{query}%%')))\
            .limit(page_size).offset(page_size*(page_number-1))
    return customer_policies

def get_specific_policy(id):
    return Policies.query.filter(id==id).first()

def get_policy_count():
    return CustomerPoliciesRelationship.query.count()

def get_visual_policies_data(region):
    customer_policies = None
    if region != 'all':
        customer_policies = CustomerPoliciesRelationship.query.with_entities(\
            func.count(CustomerPoliciesRelationship.id), Policies.dop).filter(\
            Customers.customer_region==region).join(\
            Customers, Customers.id == CustomerPoliciesRelationship.id).join(
            Policies, Policies.id == CustomerPoliciesRelationship.policy_id 
            ).group_by(func.year(Policies.dop), func.month(Policies.dop)).order_by(\
            func.year(Policies.dop), func.month(Policies.dop)).all()
    else:
        customer_policies = CustomerPoliciesRelationship.query.with_entities(\
            func.count(CustomerPoliciesRelationship.id), Policies.dop).join(\
            Policies, Policies.id == CustomerPoliciesRelationship.policy_id  \
            ).group_by(func.year(Policies.dop), func.month(Policies.dop)).order_by(\
            func.year(Policies.dop), func.month(Policies.dop)).all()
    return customer_policies