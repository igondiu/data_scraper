import logging
import pandas as pd
from flask import make_response, jsonify
from werkzeug.datastructures import FileStorage
from lib.check_data_type import check_csv_format
from lib.mysql_driver import MySQLDriver
import mysql.connector

logger = logging.getLogger(__name__)


class DataManager:
    """ Class DataManager.

    This class includes all functions to work with data in the database.

    Attributes:

    """

    def __init__(self, config):
        self.sql_driver = MySQLDriver(config)

    def post_populate_db(self, file: FileStorage):
        """ Handles the entire process of the database population with data.

        Args:
          file (FileStorage):

        Returns:

        """
        self.sql_driver.make_db_connection()
        if check_csv_format(file.filename):

            if not self.sql_driver.table_exist():
                self.sql_driver.create_table()

            try:
                df = pd.read_csv(file)
                logger.info("Inserting data from file into the database table")
                for name, row in df.iterrows():
                    # row is a tuple, we can access data doing this : row[0]
                    self.sql_driver.insert_row(row)
                self.sql_driver.db_connector.commit()
                self.sql_driver.db_connector.close()
                return make_response(jsonify({"INFO": "Inserted"}), 201)
            except UnicodeDecodeError:
                logger.warning("Input file is not correctly encoded")
                return make_response(
                    jsonify({"Warning": "The given data is not correctly encoded, can only decode UTF-8 data"}), 400)

        # ELSE file has not CSV extension
        return make_response(jsonify({"Warning": "The file has not CSV extension"}), 400)

    def get_cell_towers(self, mcc: str = None, net: str = None, area: str = None, cell: str = None):
        """

        Args:
            mcc (str):
            net (str):
            area (str):
            cell (str):

        Returns:
            List of cell towers
        """
        if mcc or net or area or cell:
            try:
                self.sql_driver.make_db_connection()
                result = self.sql_driver.select_from_table(mcc, net, area, cell)
                if result:
                    return make_response(jsonify(result), 200)
                return make_response(jsonify(
                    {"Warning": "No rows were found, make sure the input arguments are correct"}), 200)
            except mysql.connector.errors.ProgrammingError:
                logger.warning("The table doesn't exist yet, create the table and add data")
                return make_response(jsonify({"Warning": "The table was not yet created, "
                                                         "please create the table and insert data then retry"}), 200)
