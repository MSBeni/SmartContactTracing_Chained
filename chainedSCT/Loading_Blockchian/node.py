from ..extraction.database import CursorFromConnectionPool


class User:
    def __init__(self, id_, port, url):
        self.id = id_
        self.port = port
        self.url = url

    def __repr__(self):
        return "< User {} >".format(self.id)

    @staticmethod
    def create_nodes_table():
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
                CREATE TABLE IF NOT EXISTS "public"."nodes"(
                    "id" INTEGER PRIMARY KEY,
                    "port" character varying(255),
                    "url" character varying(255),
                )
                WITH (OIDS=FALSE);
                """)

                print("TABLE {} created".format('nodes'))

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
                cursor.execute('INSERT INTO nodes (id, port, url) VALUES (%s, %s, %s);',
                               (self.id, self.port, self.url))
            except:
                print("Unable to add data")

    @staticmethod
    def fetch_nodes():
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
                cursor.execute("SELECT * FROM nodes;")
                return cursor.fetchall()
            except:
                print("Failed to read the table contents ...")

    @staticmethod
    def fetch_ids():
        """
        Executing the selection of inner id of the nodes from the table
        :return:
        """
        with CursorFromConnectionPool() as cursor:
            """
            Open and close the connection --> calling connection_pool.getconn() and after committing and closing the
            connection calling the connection_pool.putconn(self.connection) to put the connection in the pool
            """
            try:
                cursor.execute("SELECT nodes.id FROM nodes;")
                print(cursor.fetchall())
            except:
                print("Failed to read the table contents ...")


    @classmethod
    def load_from_db_by_email(cls, port):
        """
        Return a user form the database based on specific port address
        port :param str: the email address of the user seeking to return
        cls :return: cls a currently bound to class Node
        """
        with CursorFromConnectionPool() as cursor:
            """
            Open and close the connection --> calling connection_pool.getconn() and after committing and closing the
            connection calling the connection_pool.putconn(self.connection) to put the connection in the pool
            """
            try:
                cursor.execute('SELECT * FROM users WHERE email=%s', (port,))
                node_data = cursor.fetchone()
                return cls(id_=node_data[0], port=node_data[1], url=node_data[2])
            except:
                print("Problem in fetching data from db")


    @classmethod
    def load_from_db_by_ids(cls, id_):
        """
        Return a node form the database based on specific id
        id :param str: the email address of the user seeking to return
        cls :return: cls a currently bound to class Node
        """
        with CursorFromConnectionPool() as cursor:
            """
            Open and close the connection --> calling connection_pool.getconn() and after committing and closing the
            connection calling the connection_pool.putconn(self.connection) to put the connection in the pool
            """
            try:
                cursor.execute('SELECT * FROM nodes WHERE id=%s', (id_,))
                user_data = cursor.fetchone()
                return cls(email=user_data[1], first_name=user_data[2], last_name=user_data[3], id_=user_data[0])
            except:
                print("Problem in fetching data from db")


    @classmethod
    def load_all_ids_from_db(cls):
        """
        Return a list of all defined ids in the db
        cls :return: cls a currently bound class od thw User
        """
        with CursorFromConnectionPool() as cursor:
            """
            Open and close the connection --> calling connection_pool.getconn() and after committing and closing the
            connection calling the connection_pool.putconn(self.connection) to put the connection in the pool
            """
            nodes_lst = []
            try:
                cursor.execute('SELECT nodes.id FROM nodes;')
                node_data = cursor.fetchall()
                nodes_lst.append(node_data)
                return nodes_lst
            except:
                print("Problem in fetching data from db")
