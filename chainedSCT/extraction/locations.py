from .database import CursorFromConnectionPool


class Location:
    def __init__(self, date_local, time_local, x_pos, y_pos, user_id=None):
        self.date_local = date_local
        self.time_local = time_local
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.user_id = user_id

    def __repr__(self):
        return "< User {} >".format(self.user_id)

    def create_locations_table(self):
        """
        Create database if it does not exist
        :return:
        """
        with CursorFromConnectionPool() as cursor:
            """
            Open and close the connection --> calling connection_pool.getconn() and after committing and closing the
            connection calling the connection_pool.putconn(self.connection) to put the connection in the pool
            """
            try:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS "public"."locations"(
                    "id" INTEGER PRIMARY KEY,
                    "date_" character varying(255),
                    "time_" character varying(255),
                    "x_pos" numeric,
                    "y_pos" numeric
                )
                WITH (OIDS=FALSE);
                """)

                print("TABLE {} created".format('locations'))

            except:
                print("Unable to create the table!!!")

    def save_loc_to_db(self):
        """
        Save the inserted data into the database
        :return:
        """
        with CursorFromConnectionPool() as cursor:
            """
            Open and close the connection --> calling connection_pool.getconn() and after closing the
            connection calling the connection_pool.putconn(self.connection) to put the connection in the pool
            --> Note: ConnectionFromPool() is no longer a direct connection so does not commit any more using 'with'
            so we should add the commit to the ConnectionFromPool class
            """
            try:
                cursor.execute('INSERT INTO locations (id, date_, time_, x_pos, y_pos) VALUES (%s, %s, %s, %s, %s);',
                               (self.user_id, self.date_local, self.time_local, self.x_pos, self.y_pos))
            except:
                print("Unable to add data")

    @staticmethod
    def fetch_loc_data():
        """
        Executing the selection of inner data of the table
        :return:
        """
        with CursorFromConnectionPool() as cursor:
            """
            Open and close the connection --> calling connection_pool.getconn() and after committing and closing the
            connection calling the connection_pool.putconn(self.connection) to put the connection in the pool
            """
            try:
                cursor.execute("SELECT * FROM locations;")
                print(cursor.fetchall())
            except:
                print("Failed to read the table contents ...")

    @staticmethod
    def fetch_loc_ids():
        """
        Executing the selection of inner id of the locations from the table
        :return:
        """
        with CursorFromConnectionPool() as cursor:
            """
            Open and close the connection --> calling connection_pool.getconn() and after committing and closing the
            connection calling the connection_pool.putconn(self.connection) to put the connection in the pool
            """
            try:
                cursor.execute("SELECT locations.user_id FROM locations;")
                print(cursor.fetchall())
            except:
                print("Failed to read the table contents ...")


