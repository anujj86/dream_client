from flask import jsonify 
from flask_restx import Resource, fields
from werkzeug.exceptions import NotFound
from src.controllers import customer_controller
from app import flask_api
from src.services.mysql_connection import MySQLConnection
from src.services.px_logging import logger

db = MySQLConnection.get_db()

api = flask_api.namespace("api/customers", description="Customers APIs")


@api.route("/<int:id>")
class Customer(Resource):
    income_group_model = flask_api.model(
        "Income Group Response Model",
        {
            "id": fields.Integer(description="Income group id"),
            "min_income": fields.Float(description="Min income"),
            "max_income": fields.Float(description="Max income")
        }
    )

    fuels_model = flask_api.model(
        "Fuels Response Model",
        {
            "id": fields.Integer(description="Fuel id"),
            "fuel_type": fields.String(description="Fuel tppe")
        }
    )

    vechile_segments_model = flask_api.model(
        "Vechile Segments Response Model",
        {
            "id": fields.Integer(description="vechile id"),
            "name": fields.Float(description="name"),
        }
    )


    get_customer_details = flask_api.model(
        "Policies Details Response Model",
        {
            "id": fields.String(description="Customer id"),
            "gender": fields.String(description="Gender"),
            "customer_region": fields.Float(description="Customer Region"),
            "income_group": fields.Nested(income_group_model, description="Income Groups", useList=False),
            "vechile_segment": fields.Nested(vechile_segments_model, description="Vechile Segments", useList=False),
            "fuels": fields.Nested(fuels_model, description="fuels")
        },
    )
    @api.response(200, "Success", get_customer_details)
    @api.response(500, "Something Went Wrong")
    def get(self, id):
        try:
            customer = customer_controller.get_specific_customer(id)
            if customer is None:
                raise NotFound(f"Customer not found")
            fuels = []
            for x in customer.vechile_segments.fuels:
                fuel_obj = {
                    "id": x.id,
                    "fuel_type": x.fuel_type
                }
                fuels.append(fuel_obj)
            obj = {
                "id": customer.id,
                "gender": customer.gender,
                "customer_region": customer.customer_region,
                "income_group": {
                    "id": customer.income.id,
                    "min_income": customer.income.min_income,
                    "max_income": customer.income.max_income
                },
                "vechile_segment": {
                    "id": customer.vechile_segments.id,
                    "name": customer.vechile_segments.name
                },
                "fuels": fuels
            }
            return jsonify(obj)
        except Exception as e:
            logger.error(f"Error while getting customer data {e}")
            return "Error while getting customer data", 500

@api.route("/region")
class Region(Resource):
    value_model = flask_api.model(
        'Value Model',
        {
            "value": fields.String(description="Region name")
        }
    )
    region_model = flask_api.model(
        'Region Model',
        {
            "data": fields.List(fields.Nested(value_model), description="List of region")
        }
    )
    @api.response(200, "Success", region_model)
    @api.response(500, "Something Went Wrong")
    def get(self):
        try:
            region_data = customer_controller.get_distinct_region()
            if region_data is None:
                raise NotFound(f"Region not found")
            regions = []
            for x in region_data:
                obj ={
                    "value": x.customer_region
                }
                regions.append(obj)
            return jsonify(regions)
        except Exception as e:
            logger.error(f"Error while getting distinct region {e}")
            return "Error while getting distinct region", 500