from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import json
from pymongo import MongoClient

zones_path = "./Controlled_Parking_Zones.geojson"
spots_path = ""
bicycle_spots_path = ""
parking_zones = open(zones_path)
zones_data = json.load(parking_zones)

mongo_client = MongoClient('localhost', 27017)
json_db = mongo_client['raw_parking_data']
collection_zones = json_db['parking_zones']
collection_zones.insert_one(zones_data)

postgres_url = URL.create(
    drivername = "postgresql", 
    username = "Lydia",  # change to your own database username
    host = "localhost",
    database = "parking"
)
# swap between the following two lines if you want to see more or less output from the postgres sql commands

postgres_engine = create_engine(postgres_url, echo=True)
# postgres_engine = create_engine(postgres_url)
postgres = postgres_engine.connect()

# NB comment the following block out for first run
postgres.execute(text("DROP TABLE parking_spots"))
postgres.execute(text("DROP TABLE parking_zones"))
postgres.execute(text("DROP TABLE hours"))
postgres.execute(text("DROP TABLE coordinates"))
postgres.execute(text("DROP TABLE vehicles"))
# end block

postgres.execute(text("CREATE TABLE vehicles (id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL)"))

# vehicle types loaded here - add here if we need more
postgres.execute(
        text("INSERT INTO vehicles (name) VALUES (:name)"),
        [{"name": "car"},{"name": "bicyle"}]
    )
postgres.execute(text("CREATE TABLE hours (id SERIAL PRIMARY KEY, start_hours VARCHAR(10), end_hours VARCHAR(10))"))
postgres.execute(text("CREATE TABLE parking_zones (id SERIAL PRIMARY KEY, council_zone_identifier VARCHAR(10) NOT NULL, price INTEGER, hours_id INTEGER REFERENCES hours(id), description VARCHAR(250), public_spaces INTEGER, permit_spaces INTEGER, disabled_spaces INTEGER )"))
postgres.execute(text("CREATE TABLE coordinates (id SERIAL PRIMARY KEY, latitude VARCHAR(20), longitude VARCHAR(20), latitude_delta VARCHAR(20), longitude_delta VARCHAR(20))"))
postgres.execute(text("CREATE TABLE parking_spots (id SERIAL PRIMARY KEY, vehicle_id INTEGER REFERENCES vehicles NOT NULL, coordinates_id INTEGER REFERENCES coordinates(id) NOT NULL, address VARCHAR(250), parking_zone_id INTEGER REFERENCES parking_zones(id), parking_info VARCHAR(300), bay_type VARCHAR(100), council_bay_identifier VARCHAR(20))"))

postgres.commit()
