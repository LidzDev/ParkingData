from sqlalchemy import create_engine, text, MetaData, Table
from sqlalchemy.engine import URL
from tables.parking_spots import insert_representative_coords, insert_prices
from tables.spot_coordinates import get_coordinates
from tables.parking_zones import get_spot_prices

print("Starting post processing the data, please stand by.")
postgres_url = URL.create(
    drivername = "postgresql", 
    username = "lydia",  # change to your own database username
    host = "localhost",
    database = "parking"
)

postgres_engine = create_engine(postgres_url)
postgres = postgres_engine.connect()
metadata = MetaData()

## getting each parking spot a single pair of coordinates
print("getting all parking spots a set of coordinates")
coordinates = get_coordinates(postgres, postgres_engine, metadata)
insert_representative_coords(postgres, coordinates)

## getting each parking spot a price
print("getting all parking spots a price")
prices = get_spot_prices(postgres, postgres_engine, metadata)
insert_prices(postgres, prices)

postgres.commit()
print("Post processing finished.")
