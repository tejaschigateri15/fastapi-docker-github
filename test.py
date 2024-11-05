# old code

from fastapi import FastAPI, status
from pydantic import BaseModel
from cassandra.cluster import Cluster, NoHostAvailable
from datetime import datetime
import uuid
import time
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class CassandraDataPopulator:
    def __init__(self, host='cassandra', port=9042, max_retries=5, retry_delay=5):
        self.host = host
        self.port = port
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.cluster = None
        self.session = None
        self._initialize_connection()

    def _initialize_connection(self):
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                print(f"Attempting to connect to Cassandra (attempt {retry_count + 1}/{self.max_retries})")
                self.cluster = Cluster([self.host], port=self.port)
                self.session = self.cluster.connect()
                self._initialize_keyspace_and_table()
                print("Successfully connected to Cassandra")
                return
            except NoHostAvailable as e:
                retry_count += 1
                if retry_count == self.max_retries:
                    raise Exception(f"Failed to connect to Cassandra after {self.max_retries} attempts: {str(e)}")
                print(f"Connection failed, retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)

    def _initialize_keyspace_and_table(self):
        self.session.execute("""
            CREATE KEYSPACE IF NOT EXISTS example_keyspace
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
        """)
        self.session.set_keyspace('example_keyspace')
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS items (
                item_id uuid PRIMARY KEY,
                name text,
                description text,
                price float,
                tax float,
                created_at timestamp
            )
        """)
        print("Schema initialization complete")

    def insert_item(self, item: Item):
        query = """
            INSERT INTO items (item_id, name, description, price, tax, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        item_id = uuid.uuid4()
        self.session.execute(query, (
            item_id,
            item.name,
            item.description,
            item.price,
            item.tax,
            datetime.now()
        ))
        return item_id

    def get_all_items(self):
        query = "SELECT * FROM items"
        rows = self.session.execute(query)
        items = []
        for row in rows:
            items.append({
                "item_id": str(row.item_id),
                "name": row.name,
                "description": row.description,
                "price": row.price,
                "tax": row.tax,
                "created_at": row.created_at,
            })
        return items

    def close(self):
        if self.cluster:
            self.cluster.shutdown()
            print("Connection closed")

# Initialize Cassandra data populator
cassandra_populator = None

@app.on_event("startup")
async def startup_event():
    global cassandra_populator
    cassandra_populator = CassandraDataPopulator()
    print("Cassandra connection initialized")

@app.on_event("shutdown")
async def shutdown_event():
    if cassandra_populator:
        cassandra_populator.close()

@app.get("/")
def hello():
    return {"Hello": "world"}

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    item_id = cassandra_populator.insert_item(item)
    return {"item_id": str(item_id), "message": "Item created successfully"}

@app.get("/items/")
def get_all_items():
    items = cassandra_populator.get_all_items()
    return items
