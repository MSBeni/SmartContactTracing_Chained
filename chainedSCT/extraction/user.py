from .database import CursorFromConnectionPool


class User:
    def __init__(self, email, first_name, last_name, id_=None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.id = id_

    def __repr__(self):
        return "< User {} >".format(self.email)

    def create_users_table(self):
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
                CREATE TABLE IF NOT EXISTS "public"."users"(
                    "id" INTEGER PRIMARY KEY,
                    "first_name" character varying(255),
                    "last_name" character varying(255),
                    "email" character varying(255)
                )
                WITH (OIDS=FALSE);
                """)

                print("TABLE {} created".format('users'))

            except:
                print("Unable to craete the table!!!")

    def create_users_location_table(self):
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
                    "date" character varying(255),
                    "time" character varying(255),
                    "X_location" FLOAT,
                    "Y_location" FLOAT
                )
                WITH (OIDS=FALSE);
                """)

                print("TABLE {} created".format('locations'))

            except:
                print("Unable to create the table!!!")

    def save_to_db(self):
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
                cursor.execute('INSERT INTO users (id, first_name, last_name, email) VALUES (%s, %s, %s, %s);',
                               (self.id, self.first_name, self.last_name, self.email))
            except:
                print("Unable to add data")

    @staticmethod
    def fetch_data():
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
                cursor.execute("SELECT * FROM users;")
                return cursor.fetchall()
            except:
                print("Failed to read the table contents ...")

    @staticmethod
    def fetch_ids():
        """
        Executing the selection of inner id of the users from the table
        :return:
        """
        with CursorFromConnectionPool() as cursor:
            """
            Open and close the connection --> calling connection_pool.getconn() and after committing and closing the
            connection calling the connection_pool.putconn(self.connection) to put the connection in the pool
            """
            try:
                cursor.execute("SELECT users.id FROM users;")
                print(cursor.fetchall())
            except:
                print("Failed to read the table contents ...")


    @classmethod
    def load_from_db_by_email(cls, email):
        """
        Return a user form the database based on specific email address
        email :param str: the email address of the user seeking to return
        cls :return: cls a currently bound class od thw User
        """
        with CursorFromConnectionPool() as cursor:
            """
            Open and close the connection --> calling connection_pool.getconn() and after committing and closing the
            connection calling the connection_pool.putconn(self.connection) to put the connection in the pool
            """
            try:
                cursor.execute('SELECT * FROM users WHERE email=%s', (email,))
                user_data = cursor.fetchone()
                return cls(email=user_data[1], first_name=user_data[2], last_name=user_data[3], id_=user_data[0])
            except:
                print("Problem in fetching data from db")


    @classmethod
    def load_from_db_by_ids(cls, id_):
        """
        Return a user form the database based on specific id
        email :param str: the email address of the user seeking to return
        cls :return: cls a currently bound class od thw User
        """
        with CursorFromConnectionPool() as cursor:
            """
            Open and close the connection --> calling connection_pool.getconn() and after committing and closing the
            connection calling the connection_pool.putconn(self.connection) to put the connection in the pool
            """
            try:
                cursor.execute('SELECT * FROM users WHERE id=%s', (id_,))
                user_data = cursor.fetchone()
                return cls(email=user_data[1], first_name=user_data[2], last_name=user_data[3], id_=user_data[0])
            except:
                print("Problem in fetching data from db")


    @classmethod
    def load_all_ids_from_db(cls):
        """
        Return a list of all defined ids in the db
        email :param str: the email address of the user seeking to return
        cls :return: cls a currently bound class od thw User
        """
        with CursorFromConnectionPool() as cursor:
            """
            Open and close the connection --> calling connection_pool.getconn() and after committing and closing the
            connection calling the connection_pool.putconn(self.connection) to put the connection in the pool
            """
            ids_lst = []
            try:
                cursor.execute('SELECT users.id FROM users;')
                user_data = cursor.fetchall()
                ids_lst.append(user_data)
                return ids_lst
            except:
                print("Problem in fetching data from db")
