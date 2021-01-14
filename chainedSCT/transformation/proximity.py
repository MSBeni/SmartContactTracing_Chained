from ..extraction import CursorFromConnectionPool


class Proximity:
    def __init__(self, date_local, user_id, contact_user_id, proximity):
        self.date_local = date_local
        self.user_id = user_id
        self.contact_user_id = contact_user_id
        self.proximity = proximity

    def __repr__(self):
        return "< User {} >".format(self.init_user_id)

    @staticmethod
    def create_proximity_table():
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
                CREATE TABLE IF NOT EXISTS "public"."proximity"(
                    "pos_date" DATE NOT NULL,
                    "user_id" int4 NOT NULL,
                    "contact_id" int4 NOT NULL,
                    "proximity"  numeric(10,4)
                )
                WITH (OIDS=FALSE);
                """)

                print("TABLE {} created".format('proximity'))

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
                cursor.execute('INSERT INTO proximity (pos_date, user_id, contact_id, proximity) VALUES '
                               '(%s, %s, %s, %s);',
                               (self.date_local, self.user_id, self.contact_user_id, self.proximity))
            except:
                print("Unable to add data")

    @staticmethod
    def fetch_proximity_data():
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
                cursor.execute("SELECT * FROM proximity;")
                print(cursor.fetchall())
            except:
                print("Failed to read the table contents ...")

    @staticmethod
    def fetch_proximity_ids():
        """
        Executing the selection of inner id of the proximity from the table
        :return:
        """
        with CursorFromConnectionPool() as cursor:
            """
            Open and close the connection --> calling connection_pool.getconn() and after committing and closing the
            connection calling the connection_pool.putconn(self.connection) to put the connection in the pool
            """
            try:
                cursor.execute("SELECT proximity.user_id FROM proximity;")
                print(cursor.fetchall())
            except:
                print("Failed to read the table contents ...")


