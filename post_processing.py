from sqlalchemy import create_engine, text, MetaData, Table
from sqlalchemy.engine import URL
from tables.parking_spots import insert_representative_coords

postgres_url = URL.create(
    drivername = "postgresql", 
    username = "lydia",  # change to your own database username
    host = "localhost",
    database = "parking"
)

postgres_engine = create_engine(postgres_url)
postgres = postgres_engine.connect()
metadata = MetaData()
spot_coordinates_table = Table('spot_coordinates', metadata)

Table(
    'spot_coordinates',
    metadata,
    autoload_with=postgres_engine,
    extend_existing=True
)

query =  text("""
SELECT DISTINCT ON (parking_spots_id) * from spot_coordinates ORDER BY parking_spots_id 
    """)
result = postgres.execute(query)
result_set = result.fetchall()

insert_representative_coords(postgres, result_set)
postgres.commit()
