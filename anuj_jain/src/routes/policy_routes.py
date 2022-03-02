import sqlalchemy
from flask import jsonify, request
from flask_restx import Resource, fields, reqparse
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from src.controllers import policy_controller
from app import flask_api
from src.services.mysql_connection import MySQLConnection
from src.services.px_logging import logger

db = MySQLConnection.get_db()

api = flask_api.namespace("api/policies", description="Policies APIs")

@api.route("/")
class PoliciesAll(Resource):
    value = flask_api.model("policy model",
        {
            "policy_id": fields.String(description="Policy Id"),
            "customer_id": fields.String(description="Customer id"),
            "dop": fields.DateTime(description="Date of purchase"),
            "premium": fields.Float(description="Premium"),
            "body_injury_libality": fields.Boolean(description="Body injury libality"),
            "property_damage_libality": fields.Boolean(description="Property damage libality"),
            "collision": fields.Boolean(description="Collision"),
            "comprehensive": fields.Boolean(description="Comprehensive")            
        }
    )
    get_all_policies = flask_api.model(
        "Policies Details Response Model",
        {
            "data": fields.List(fields.Nested(value), description="list of policies"),
            "count": fields.Integer(description="Total policies count")
        }
    )
    parser = reqparse.RequestParser()
    parser.add_argument(
        "page_number", type=int, help="Page number to return the results from"
    )
    parser.add_argument("page_size", type=int, help="Page size")
    parser.add_argument("query", help="Search query")
    @api.response(200, "Success", get_all_policies)
    @api.response(500, "Something Went Wrong")
    @api.expect(parser)
    def get(self):
        try:
            page_number = 1
            page_size = 5
            args = request.args
            if args.get("page_size") is not None:
                page_size = int(args.get("page_size"))
            if args.get("page_number") is not None:
                page_number = int(args.get("page_number"))
            query = args.get("query", None)
            customer_policies = policy_controller.get_all_policies(query, page_size, page_number)
            if customer_policies is None:
                logger.info(f"Policies not found")
                raise NotFound(f"Policies not found")
            policies = []
            for policy in customer_policies:
                p = policy_controller.get_specific_policy(policy.policy_id)
                obj = {
                    "policy_id": policy.policy_id,
                    "customer_id": policy.customer_id,
                    "martial_status": policy.maritial_status,
                    "dop": str(p.dop),
                    "premium": p.premium,
                    "body_injury_libality": p.body_injury_libality,
                    "property_damage_libality": p.property_damage_libality,
                    "collision": p.collision,
                    "comprehensive": p.comprehensive            
                }
                policies.append(obj)
            return jsonify({"data": policies, "count": policy_controller.get_policy_count()})
        except Exception as e:
            logger.error(f"Error while getting all policies {e}")
            return "Error while getting all policies", 500


@api.route("/<int:id>")
class EditPolicy(Resource):
    edit_policy = flask_api.model(
        'Edit Policies',
        {
            "premium": fields.Float(description="Premium", required=True),
            "body_injury_libality": fields.Boolean(description="Body injury libality", required=True),
            "property_damage_libality": fields.Boolean(description="Property damage libality", required=True),
            "collision": fields.Boolean(description="Collision", required=True),
            "comprehensive": fields.Boolean(description="Comprehensive", required=True)
        }
    )

    @api.response(200, "Success")
    @api.response(500, "Something Went Wrong")
    @api.expect(edit_policy, validate=True)
    def put(self, id):
        try:
            json_data = request.json
            print(json_data)
            if json_data['premium'] > 1000000:
                raise BadRequest(f"Premium should not be greater than one million {json_data['premium']}")
            policy = policy_controller.get_specific_policy(id)
            print(policy)
            if policy is None:
                raise NotFound(f"Policy not found")
            policy.premium = json_data["premium"]
            policy.body_injury_libality = json_data["body_injury_libality"]
            policy.property_damage_libality = json_data["property_damage_libality"]
            policy.collision = json_data["collision"]
            policy.comprehensive = json_data["comprehensive"]
            try:
                db.session.commit()
                return jsonify({"success": True})
            except sqlalchemy.exc.IntegrityError:
                raise Conflict(f"Error while updating policy")
        except Exception as e:
            logger.error(f"Error while editing policy {e}")
            return "Error while editing policy", 500


@api.route("/visual-graph/<string:region>")
class VisualGraph(Resource):

    value = flask_api.model(
        "value",
        {
            "x": fields.DateTime(description="value"),
            "y": fields.Integer(description="value")
        }
    )

    get_visual_data = flask_api.model(
        'Visual data model',
        {
            "data": fields.List(fields.Nested(value), description="Visual Data")
        }
    )
    @api.response(200, "Success", get_visual_data)
    @api.response(500, "Something Went Wrong")
    def get(self, region):
        try:
            customer_policies = policy_controller.get_visual_policies_data(region)
            if customer_policies is None:
                raise NotFound(f"Policies not found")
            policies = []
            for x in customer_policies:
                obj = {
                    "x": str(x.dop),
                    "y": x[0]
                }
                policies.append(obj)
            return jsonify({"data": policies})
        except Exception as e:
            logger.error(f"Error while getting graph data {e}")
            return "Error while getting graph data", 500