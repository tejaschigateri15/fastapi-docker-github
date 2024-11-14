from cassandra.cluster import Cluster
import uuid
from models import Book,NewUser,LoginUser

class CassandraDataPopulator:
    def __init__(self, host='cassandra', port=9042):
        self.host = host
        self.port = port
        self.cluster = None
        self.session = None
        self._initialize_connection()

    def _initialize_connection(self):
        print("Attempting to connect to Cassandra")
        self.cluster = Cluster([self.host], port=self.port)
        self.session = self.cluster.connect()
        self._initialize_keyspace_and_table()
        print("Successfully connected to Cassandra")

    def _initialize_keyspace_and_table(self):
        self.session.execute("""
            CREATE KEYSPACE IF NOT EXISTS example_keyspace
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
        """)
        self.session.set_keyspace('example_keyspace')
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id uuid PRIMARY KEY,
                name text,
                author text,              
            )
        """)
        self.session.execute(
            """
                CREATE TABLE IF NOT EXISTS user_records (
                    username text PRIMARY KEY ,
                    email text,
                    password text
                )
            """
        )
        print("Schema initialization complete")


    def get_all_books(self):
        query = "SELECT * FROM books"
        rows = self.session.execute(query)
        books = []
        for row in rows:
            books.append({
                "id": str(row.id),
                "name": row.name,
                "author": row.author,

            })
        return books


    def ret_specific_book(self, id):
        query = "SELECT * FROM books WHERE id = %s"
        book = self.session.execute(query, (id,))
        books = []
        for row in book:
            books.append({
                "id": str(row.id),
                "name": row.name,
                "author": row.author,
            })
        return books


    def insert_book(self, book: Book):
        query = """
            INSERT INTO books (id, name, author)
            VALUES (%s, %s, %s)
        """
        id = uuid.uuid4()
        self.session.execute(query, (
            id,
            book.name,
            book.author
        ))
        return id


    def create_new_user(self,user:NewUser):
        query = "Insert into user_records (username,email,password) values (%s,%s,%s)"
        self.session.execute(query,(user.username,user.email,user.password))
        return {"message": f"{user.username} user created"}


    def verify_user(self,login:LoginUser):
        query = "select username,password from user_records where username = %s"
        user = self.session.execute(query,(login.username,)).one()
        print(user)
        if not user:
            return {"message": "User not found", "status": "error"}
        elif login.password == user.password:
            return {
                "message": "Login successful",
                "status": "success",
                "username": user.username
            }
        else:
            return {
                "message": "Invalid password",
                "status": "error"
            }

    def close(self):
        if self.cluster:
            self.cluster.shutdown()
            print("Connection closed")
