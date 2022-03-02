import logging
import sys
import os
from flask_sqlalchemy import SQLAlchemy

from app import app

logger = logging.getLogger(__name__)

from flask_migrate import Migrate


from config import config

class MySQLConnection:
    db = None

    @staticmethod
    def initialize():
        try:
            MySQLConnection.db = SQLAlchemy(app)
        except Exception as e:
            logger.error(f"MySQL connection failed: {e}")
            sys.exit(-1)

    @staticmethod
    def get_db():
        if MySQLConnection.db is None:
            MySQLConnection.initialize()

        return MySQLConnection.db
    
    
    @staticmethod
    def get_migration():
        directory = config.MIGRATION_DIR
        if MySQLConnection.db is None:
                MySQLConnection.initialize()
        MySQLConnection.migrate = Migrate(app, MySQLConnection.db, directory=directory, compare_type=True)
        return  MySQLConnection.migrate