from models.customers import Customers

def get_specific_customer(id):
    return Customers.query.filter_by(id=id).first()

def get_distinct_region():
    return Customers.query.with_entities(Customers.customer_region).group_by(\
        Customers.customer_region).order_by(Customers.customer_region).all()