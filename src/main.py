import logging
import os
import sys

from flask import Flask, request, make_response, jsonify
from flask_restx import Api, Resource

sys.path.append(os.path.dirname(os.path.abspath("./app")))
import config.config as cfg
from src.setup.setup import logger_setup
from src.setup.flask_app import run_flask_app
from src.data_manager import DataManager


logger = logging.getLogger(__name__)
data_manager = DataManager(cfg)

app = Flask(__name__)
API = Api(
    app,
    title="TEST UPCITI API",
    description="Documentation of the API of the data scraper module",
    doc="/doc",
    prefix="/test_upciti/api/v1",
)

STATUS_NS = API.namespace("STATUS", path="/")
POPULATE_DB_NS = API.namespace("Populate database", path="/")
GET_CELL_TOWER_NS = API.namespace("Get a list of cell towers", path="/")


@app.route("/")
@app.route("/test_upciti/api/v1/")
def home():
    """ Default method : returns a simple page """
    return "<h1>TEST UPCITI API</h1><p>This is the first version of the API! Enjoy :).</p>"


@POPULATE_DB_NS.route('/populate_db', methods=["POST"])
class PopulateDB(Resource):
    @POPULATE_DB_NS.response(201, "Success")
    @POPULATE_DB_NS.response(400, "Bad input parameter")
    @POPULATE_DB_NS.response(500, "Internal server error")
    @POPULATE_DB_NS.doc(description="Populates the database with the data received in input")
    @POPULATE_DB_NS.param(
        "file", "The CSV file containing the dataset", "formData", required=True, type="file"
    )
    def post(self):
        """ Insert into the database rows from input file """
        if request.method == "POST":
            logger.info("POST request on [/test_upciti/api/v1/populate_db] received")
            try:
                file = request.files["file"]
                result = data_manager.post_populate_db(file)
                return result
            except Exception as e:
                logger.exception("An error has occurred in the function POST() of the class PopulateDB : ".format(e))
                return make_response(jsonify({"ERROR": "Internal server error"}), 500)


@GET_CELL_TOWER_NS.route('/get_cell_towers/<string:MCC>&<string:Net>&<string:Area>&<string:Cell>', methods=["GET"])
class GetCellTower(Resource):
    @GET_CELL_TOWER_NS.response(200, "Success")
    @GET_CELL_TOWER_NS.response(400, "Bad input parameter")
    @GET_CELL_TOWER_NS.response(500, "Internal server error")
    @GET_CELL_TOWER_NS.doc(description="Gets a list of cell towers from the database")
    @GET_CELL_TOWER_NS.param(
        "MCC", "The MCC of the tower", "path", required=False
    )
    @GET_CELL_TOWER_NS.param(
        "Net", "The Net of the tower", "path", required=False
    )
    @GET_CELL_TOWER_NS.param(
        "Area", "The Area of the tower", "path", required=False
    )
    @GET_CELL_TOWER_NS.param(
        "Cell", "The Cell of the tower", "path", required=False
    )
    def get(self, MCC, Net, Area, Cell):
        """ Fetch rows from the database """
        if request.method == "GET":
            logger.info("GET request on [/test_upciti/api/v1/get_cell_towers] received")
            try:
                if MCC == "undefined" or MCC == '{MCC}':
                    MCC = None
                if Net == "undefined" or Net == '{Net}':
                    Net = None
                if Area == "undefined" or Area == '{Area}':
                    Area = None
                if Cell == "undefined" or Cell == '{Cell}':
                    Cell = None
                result = data_manager.get_cell_towers(MCC, Net, Area, Cell)
                return result
            except Exception as e:
                logger.exception("An error has occurred in the function GET() of the class GetCellTower".format(e))
                return make_response(jsonify({"ERROR": "Internal server error"}), 500)


@app.errorhandler(404)
def not_found(error):
    """ Function is called when the requested page was not found.

        Args:
            error: http_error (404 not found)
        Returns:
            http_response (404 not found)
    """
    return make_response(jsonify({'ERROR': '{}'.format(error)}), 404)


def main(config, flask_app):
    """Run the flask web application

        Args:
            flask_app (app): Flask application
            config (config file)
        """
    logger_setup(config)
    run_flask_app(flask_app)


if __name__ == '__main__':
    main(cfg, app)
