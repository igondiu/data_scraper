import logging
import mysql.connector

logger = logging.getLogger(__name__)


class MySQLDriver:
    """ Class MySQLDriver.

    This class includes all functions to work with MySQL database.

    Attributes:

    """

    def __init__(self, config):
        self.host = config.MYSQL_HOST
        self.user = config.MYSQL_USER
        self.password = config.MYSQL_PASSWORD
        self.database = config.MYSQL_DATABASE
        self.db_connector = None
        self.db_cursor = None

    def make_db_connection(self):
        self.db_connector = mysql.connector.connect(
            host=self.host, user=self.user, password=self.password, database=self.database)
        self.db_cursor = self.db_connector.cursor()

    def table_exist(self):
        try:
            query = "SELECT count(*) FROM information_schema.TABLES " \
                    "WHERE TABLE_SCHEMA = '{}' " \
                    "AND TABLE_NAME = 'cell_towers' ".format(self.database)
            self.db_cursor.execute(query)
            result = self.db_cursor.fetchone()
            if result[0] > 0:
                return True
            return False
        except Exception as e:
            logger.exception("An exception has occurred in function table_exists() : {}".format(e))

    def create_table(self):
        try:
            query = "CREATE TABLE cell_towers (radio VARCHAR(10), mcc INT(10), net INT(10), area INT(10), " \
                    "cell INT(10), unit INT(10), lon FLOAT(15), lat FLOAT(15), cell_range INT(10), samples INT(10), " \
                    "changeable INT(2), created INT(10), updated INT(10), averageSignal INT(2), " \
                    "PRIMARY KEY (mcc, net, area, cell))"
            self.db_cursor.execute(query)
            self.db_connector.commit()
        except Exception as e:
            logger.exception("An exception has occurred in function create_table() : {}".format(e))
            self.db_connector.rollback()

    def insert_row(self, row: tuple):
        """ Insert in the table values received in param.

        Args:
            row (tuple): contains the row with the data from the input CSV file

        Returns:
            True if successfully inserted, false otherwise
        """
        try:
            query = "INSERT INTO cell_towers VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', " \
                    "'{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}')".format(
                        row[0], row[1], row[2], row[3], row[4], row[4], row[5], row[6], row[7], row[8], row[9],
                        row[10], row[11], row[12], row[13])
            self.db_cursor.execute(query)
        except mysql.connector.errors.IntegrityError:
            logger.info("Row exists already in database")
        except Exception as e:
            logger.exception("An exception has occurred in function insert_row() : {}".format(e))
            self.db_connector.rollback()
            raise Exception("Something went wrong while inserting data in the table, logs are available for more info")

    def select_from_table(self, mcc: str = None, net: str = None, area: str = None, cell: str = None):
        """ Selects from the table a list of rows and returns them

        Args:
            mcc (str):
            net (str):
            area (str):
            cell (str):

        Returns:
            List of rows
        """
        query = "SELECT * FROM cell_towers WHERE "
        if mcc is not None:
            query = query + "mcc = '{}'".format(mcc)
            if net is not None:
                query = query + "and net = '{}'".format(net)
            if area is not None:
                query = query + "and area = '{}'".format(area)
            if cell is not None:
                query = query + "and cell = '{}'".format(cell)
        elif net is not None:
            query = query + "net = '{}'".format(net)
            if area is not None:
                query = query + "and area = '{}'".format(area)
            if cell is not None:
                query = query + "and cell = '{}'".format(cell)
        elif area is not None:
            query = query + "area = '{}'".format(area)
            if cell is not None:
                query = query + "and cell = '{}'".format(cell)
        elif cell is not None:
            query = query + "cell = '{}'".format(cell)
        else:
            return None

        self.db_cursor.execute(query)
        result = self.db_cursor.fetchall()
        if result:
            return result
        return None
