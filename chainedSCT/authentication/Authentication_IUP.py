from ..extraction.database import CursorFromConnectionPool


class Infection:
    def __init__(self, user_id, infection, date_):
        self.user_id = user_id
        self.infection = infection
        self.date_ = date_

    def __repr__(self):
        return "< User {} >".format(self.user_id)

    @staticmethod
    def create_infection_table():
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
                DROP TABLE IF EXISTS "public"."infection";
                CREATE TABLE IF NOT EXISTS "public"."infection"(
                    "user_id" int4 NOT NULL,
                    "status" BOOLEAN NOT NULL,
                    "date_" TIME NOT NULL,
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
                cursor.execute('INSERT INTO infection (user_id, status, date_) VALUES '
                               '(%s, %s, %s);',
                               (self.user_id, self.infection, self.date_))
            except:
                print("Unable to add data")

    @staticmethod
    def fetch_infection_data():
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
                cursor.execute("SELECT * FROM infection;")
                return cursor.fetchall()
            except:
                print("Failed to read the table contents ...")

    @staticmethod
    def fetch_infection_ids():
        """
        Executing the selection of inner id of the infected users from the table
        :return:
        """
        with CursorFromConnectionPool() as cursor:
            """
            Open and close the connection --> calling connection_pool.getconn() and after committing and closing the
            connection calling the connection_pool.putconn(self.connection) to put the connection in the pool
            """
            try:
                cursor.execute("SELECT infection.user_id FROM infection;")
                return cursor.fetchall()
            except:
                print("Failed to read the table contents ...")

    @staticmethod
    def fetch_infection_dates():
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
                cursor.execute("SELECT infection.date_ FROM infection WHERE infection.status=true;")
                infection_data = cursor.fetchall()
                dates_lst.append(infection_data)
                return dates_lst
            except:
                print("Failed to read the table contents ...")



    @staticmethod
    def fetch_infection_ids_by_date(date):
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
                cursor.execute("SELECT infection.user_id FROM infection WHERE infection.status=true AND "
                               "infection.date_=?;", (date,))
                all_users_id = cursor.fetchall()
                uniqe_users_in_a_day.append(all_users_id)
                return uniqe_users_in_a_day
            except:
                print("Failed to read the table contents ...")



class IUP:
    def __init__(self, id_, infection_date):
        self.id = id_
        self.infection_date = infection_date




