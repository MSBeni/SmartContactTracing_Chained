from .database import CursorFromConnectionPool


class Location:
    def __init__(self, user_id, date_local, time_local, x_pos, y_pos):
        self.date_local = date_local
        self.time_local = time_local
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.user_id = user_id

    def __repr__(self):
        return "< User {} >".format(self.user_id)

    @staticmethod
    def create_locations_table():
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
                DROP TABLE IF EXISTS "public"."locations";
                CREATE TABLE IF NOT EXISTS "public"."locations"(
                    "user_id" int4 NOT NULL,
                    "pos_date" DATE NOT NULL,
                    "pos_time" TIME NOT NULL,
                    "x_pos"  numeric(10,4),
                    "y_pos"  numeric(10,4)
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
                cursor.execute('INSERT INTO locations (user_id, pos_date, pos_time, x_pos, y_pos) VALUES '
                               '(%s, %s, %s, %s, %s);',
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


    @staticmethod
    def fetch_loc_dates():
        """
        Executing the selection of inner id of the locations from the table
        :return:
        """
        dates_lst = []
        with CursorFromConnectionPool() as cursor:
            """
            Open and close the connection --> calling connection_pool.getconn() and after committing and closing the
            connection calling the connection_pool.putconn(self.connection) to put the connection in the pool
            """
            try:
                cursor.execute("SELECT locations.pos_date FROM locations;")
                location_data = cursor.fetchall()
                dates_lst.append(location_data)
                return dates_lst
            except:
                print("Failed to read the table contents ...")



    @staticmethod
    def fetch_proximity_ids_by_date(date):
        """
        Executing the selection of inner id of the proximity from the table
        :return:
        """
        with CursorFromConnectionPool() as cursor:
            """
            Open and close the connection --> calling connection_pool.getconn() and after committing and closing the
            connection calling the connection_pool.putconn(self.connection) to put the connection in the pool
            """
            uniqe_users_in_a_day = []
            try:
                cursor.execute("SELECT locations.user_id FROM locations WHERE locations.pos_date=(%s);",
                               (date,))
                all_users_id = cursor.fetchall()
                uniqe_users_in_a_day.append(all_users_id)
                return uniqe_users_in_a_day
            except:
                print("Failed to read the table contents ...")


    @staticmethod
    def fetch_proximity_loc_by_date_id(date, _user_id):
        """
        Executing the selection of inner id of the proximity from the table
        :return:
        """
        with CursorFromConnectionPool() as cursor:
            """
            Open and close the connection --> calling connection_pool.getconn() and after committing and closing the
            connection calling the connection_pool.putconn(self.connection) to put the connection in the pool
            """
            user_location_in_a_day = []
            try:
                cursor.execute("SELECT locations.x_pos, locations.y_pos FROM locations "
                               "WHERE locations.pos_date=(%s) AND locations.user_id=(%s);", (date, _user_id))
                all_users_locs = cursor.fetchall()
                user_location_in_a_day.append(all_users_locs)
                return user_location_in_a_day
            except:
                print("Failed to read the table contents ...")



