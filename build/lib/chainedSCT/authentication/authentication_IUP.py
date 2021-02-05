from ..extraction.database import CursorFromConnectionPool
import json
# from bson import json_util

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
                    "date_" TIME NOT NULL
                )
                WITH (OIDS=FALSE);
                """)

                print("TABLE {} created".format('infection'))

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
        Executing the selection of inner id of the infection from the table
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

    def __repr__(self):
        return "< User {} >".format(self.id)

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
                DROP TABLE IF EXISTS "public"."iup";
                CREATE TABLE "public"."iup"(
                    "id" int4 NOT NULL,
                    "infection_date" DATE NOT NULL
                )
                WITH (OIDS=FALSE);
                """)

                print("TABLE {} created".format('IUP'))

            except:
                print("Unable to create the table!!!")

    def save_infected_users_to_db(self):
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
            # cursor.execute('INSERT INTO iup (id, infection_date) VALUES (%s, %s);', (self.id, self.infection_date))
            try:
                cursor.execute('INSERT INTO iup (id, infection_date) VALUES '
                               '(%s, %s);',
                               (self.id, self.infection_date))
            except:
                print("Unable to add data")

    @classmethod
    def fetch_iup_data(cls):
        """
        Executing the selection of inner data of the table
        :return:
        """
        with CursorFromConnectionPool() as cursor:
            """
            Open and close the connection --> calling connection_pool.getconn() and after committing and closing the
            connection calling the connection_pool.putconn(self.connection) to put the connection in the pool
            """
            inf_user = []
            try:
                cursor.execute("SELECT * FROM iup;")
                data = cursor.fetchall()
                for infected_user in data:
                    inf_user.append({"user": (infected_user[0], infected_user[1].isoformat())})
                return inf_user
            except:
                print("Failed to read the table contents ...")

    @classmethod
    def fetch_iup_ids(cls):
        """
        Executing the selection of ids of the infected users
        :return: list of infected users id fetched from the IUP database
        """
        with CursorFromConnectionPool() as cursor:
            """
            Open and close the connection --> calling connection_pool.getconn() and after committing and closing the
            connection calling the connection_pool.putconn(self.connection) to put the connection in the pool
            """
            inf_user_ids = []
            try:
                cursor.execute("SELECT iup.id FROM iup;")
                data = cursor.fetchall()
                for infected_user_id in data:
                    inf_user_ids.append(infected_user_id[0])
                return inf_user_ids
            except:
                print("Failed to read the table contents ...")


# Save the authorized users from the private document into authcheck DB
class AuthorizedUsers:
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password

    @staticmethod
    def create_authcheck_table():
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
                    DROP TABLE IF EXISTS "public"."authcheck";
                    CREATE TABLE "public"."authcheck" (
                    "user_id" INTEGER NOT NULL,
                    "username" character varying(255),
                    "password" character varying(255)
                )
                WITH (OIDS=FALSE);
                """)

                print("TABLE {} created".format('authcheck'))

            except:
                print("Unable to create the table!!!")

    def save_authorized_users_to_db(self):
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
                cursor.execute('INSERT INTO authcheck (user_id, username, password) VALUES '
                               '(%s, %s, %s);',
                               (self.user_id, self.username, self.password))
            except:
                print("Unable to add data")

    @staticmethod
    def fetch_authorized_id():
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
                cursor.execute("SELECT authcheck.user_id FROM authcheck;")
                user_ids = cursor.fetchall()
                return [el[0] for el in user_ids]
            except:
                print("Failed to read the table contents ...")


    @staticmethod
    def fetch_authorized_username():
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
                cursor.execute("SELECT authcheck.username FROM authcheck;")
                user_names = cursor.fetchall()
                return [el[0] for el in user_names]
            except:
                print("Failed to read fetch_authorized_username in the table {} contents ...".format('authcheck'))


    @staticmethod
    def password_check_for_username(username_):
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
                cursor.execute("SELECT authcheck.password FROM authcheck WHERE username=%s", (username_,))
                return cursor.fetchone()

            except:
                print("Failed to read the table contents ...")


    @staticmethod
    def id_check_for_username(username_):
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
                cursor.execute("SELECT authcheck.user_id FROM authcheck WHERE username=%s", (username_,))
                return cursor.fetchone()

            except:
                print("Failed to read the table contents ...")


class AuthAcceptedUsers:
    def __init__(self, user_id, username, password):
        self.id = user_id
        self.username = username
        self.password = password

    @staticmethod
    def create_iupmanagers_table():
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
                DROP TABLE IF EXISTS "public"."iupmanagers";
                CREATE TABLE "public"."iupmanagers"(
                    "id" int4 NOT NULL,
                    "username" text NOT NULL,
                    "password" text NOT NULL
                )
                WITH (OIDS=FALSE);
                """)

                print("TABLE {} created".format('iupmanagers'))

            except:
                print("Unable to create the table!!!")

    def save_accepted_auth_to_db(self):
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
                cursor.execute('INSERT INTO iupmanagers (id, username, password) VALUES (%s, %s, %s);',
                               (self.id, self.username, self.password))
            except:
                print("Unable to add data")


    @classmethod
    def get_authenticated_user_by_username(cls, username_):
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
                cursor.execute("SELECT * FROM iupmanagers WHERE username=%s;", (username_,))
                user_ = cursor.fetchone()
                if user_:
                    user_f = cls(*user_)
                else:
                    user_f = None

                return user_f
            except:
                return "Failed to read the table {} contents ...".format('iupmanagers')

    @classmethod
    def get_authenticated_user_by_id(cls, identity):
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
                cursor.execute("SELECT * FROM iupmanagers WHERE id=%s;", (identity,))
                user_ = cursor.fetchone()
                print(*user_)
                if user_:
                    user_f = cls(*user_)
                else:
                    user_f = None

                return user_f
            except:
                return "Failed to read the table {} contents ...".format('iupmanagers')


    @staticmethod
    def fetch_All_authorized_IUP(identity):
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
                cursor.execute("SELECT * FROM iupmanagers WHERE id=%s;", (identity,))
                return cursor.fetchone()
            except:
                print("Failed to read the table contents ...")


