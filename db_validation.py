import pymysql.cursors
import pymysql.connections
import sys
import os


class DBValidation:
    """DB Schema validation."""

    def __init__(self, version: str) -> None:
        """Set a version and create the DB conenction.
        :param version: Schema version.
        :type version: str
        """
        self.version = version
        self.connection = self.db_connect()

    def db_connect(self) -> pymysql.connections.Connection:
        """Create a DB connection.
        :return: db connection.
        :rtype: pymysql.connections.Connection
        """
        connection = pymysql.connect(
            host="db nae",
            user="uname",
            password="pwd",
            database="tests",
            cursorclass=pymysql.cursors.DictCursor,
        )
        return connection

    def check_if_version_exists(self, schemas_list: list) -> bool:
        """Check if schema versoin is in the DBs list.
        :param schemas_list: List of Schema from the DB
        :type schemas_list: list
        :return: True if version exists.
        :rtype: bool
        """
        return True if f"tests{self.version}" in schemas_list else False

    def get_db_list(self) -> bool:
        """Get all databases.
        :return: True if version exists in DB.
        :rtype: bool
        """
        with self.connection.cursor() as cursor:
            sql = "SHOW DATABASES"
            cursor.execute(sql)
            result = cursor.fetchall()
            dbs = [list(db.values())[0] for db in result]
            print("List of databases:")
            print(dbs)
            return self.check_if_version_exists(dbs)

    def create_db(self) -> str:
        """create db schema.

        :param version: Current version
        :type version: str
        :return: schema name.
        :rtype: str
        """
        db_name = f"tests{self.version}"
        schema_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "tests_schema.sql"
        )
        print(f"schema file: {schema_file}")
        stmts = self.parse_sql(schema_file, db_name)
        with self.connection.cursor() as cursor:
            for stmt in stmts:
                cursor.execute(stmt)
            self.connection.commit()
        return db_name

    def parse_sql(self, filename: str, db_name: str) -> list:
        """Parsing a given sql file to list of statement.
        :param filename: file name path.
        :type filename: str
        :param db_name: The db schema name.
        :type db_name: str
        :return: List of statement.
        :rtype: list
        """
        data = open(filename, "r").readlines()
        stmts = []
        DELIMITER = ";"
        stmt = ""

        for lineno, line in enumerate(data):
            if not line.strip():
                continue

            if line.startswith("--"):
                continue

            if "tests$ver" in line:
                # Replace the next string with our testsX.Y.0 version.
                line = line.replace("tests$ver", db_name)

            if "DELIMITER" in line:
                DELIMITER = line.split()[1]
                continue

            if DELIMITER not in line:
                stmt += line.replace(DELIMITER, ";")
                continue

            if stmt:
                stmt += line
                stmts.append(stmt.strip())
                stmt = ""
            else:
                stmts.append(line.strip())
        return stmts

    def schema_counter(self, db_name: str) -> int:
        """Count database tables.
        :param db_name: DB name
        :type db_name: str
        :return: Schema counter.
        :rtype: int
        """
        with self.connection.cursor() as cursor:
            sql = f"SELECT count(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{db_name}'"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(f"Schema tables counter result: {result}")
            return result[0]["count(*)"]

    def db_connection_main(self):
        """Handle db validation process."""

        is_exist = self.get_db_list()
        print(f"DB is exists:{is_exist}")
        if is_exist:
            self.connection.close()
            return
        else:
            db_name = self.create_db()
            is_exist = self.get_db_list()
            print(f"Is schema created: {is_exist}")
            count = self.schema_counter(db_name)
            self.connection.close()
            if count < 1:
                print(
                    f"Counter is less than 1, Schema not created successfully, exit now."
                )
                sys.exit(1)


if __name__ == "__main__":
    args = sys.argv[1:]
    ver = f"{args[0][0:3]}.0"
    # ver = '7.3.0' # for debugging
    print(f"Main version: {ver}")
    db_validation_cls = DBValidation(ver)
    db_validation_cls.db_connection_main()
