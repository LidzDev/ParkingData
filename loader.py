import json
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from pymongo import MongoClient
from tables.vehicles import create_vehicles_table
from tables.hours import create_hours_table
from tables.parking_zones import create_parking_zones_table, add_parking_zones_data, add_price_data
from tables.zone_coordinates import create_zone_coordinates_table, insert_polygon_coordinates_data
from tables.parking_spots import create_parking_spots_table
from tables.spot_coordinates import create_spot_coordinates_table, input_spot_coordinates_data
from tables.bicycle_spots import create_bicycle_spots_table, input_bicycle_data

zones_path = "./Controlled_Parking_Zones.geojson"
spots_path = "./Parking_bays.geojson"
bicycle_spots_path = "./Bicycle_spots.json"

parking_zones = open(zones_path)
parking_spots = open(spots_path)
bicycle_spots = open(bicycle_spots_path)

zones_data = json.load(parking_zones)
spots_data = json.load(parking_spots)
bicycle_data = json.load(bicycle_spots)

mongo_client = MongoClient('localhost', 27017)
json_db = mongo_client['raw_parking_data']

collection_zones = json_db['parking_zones']
collection_zones.drop()
collection_zones.insert_one(zones_data)
parking_zones.close()

collection_spots = json_db['parking_spots']
collection_spots.drop()
collection_spots.insert_one(spots_data)
parking_spots.close()

collection_bicycle_spots = json_db['bicycle_spots']
collection_bicycle_spots.drop()
collection_bicycle_spots.insert_one(bicycle_data)
bicycle_spots.close()

postgres_url = URL.create(
    drivername = "postgresql", 
    username = "darrenlackie",  # change to your own database username
    host = "localhost",
    database = "parking"
)

# swap between the following two lines if you want to see more or less output from the postgres sql commands
postgres_engine = create_engine(postgres_url, echo=True)
#postgres_engine = create_engine(postgres_url)
postgres = postgres_engine.connect()

postgres.execute(text("DROP TABLE IF EXISTS parking_spots"))
postgres.execute(text("DROP TABLE IF EXISTS parking_zones"))
postgres.execute(text("DROP TABLE IF EXISTS hours"))
postgres.execute(text("DROP TABLE IF EXISTS zone_coordinates"))
postgres.execute(text("DROP TABLE IF EXISTS spot_coordinates"))
postgres.execute(text("DROP TABLE IF EXISTS vehicles"))
postgres.execute(text("DROP TABLE IF EXISTS bicycle_spots"))

## vehicle table creation

create_vehicles_table(postgres)

## hours table creation

create_hours_table(postgres)

## parking spot coordinates table creation

create_spot_coordinates_table(postgres)

## parking zones table creation

create_parking_zones_table(postgres)

## coordinates table creation

create_zone_coordinates_table(postgres)

## parking spots table creation

create_parking_spots_table(postgres)

## Selected Parking zone Data read in from json

add_parking_zones_data(postgres, zones_data)

## entering price data for parking zones

add_price_data(postgres)

## entering coordinate data for parking zone polygons

insert_polygon_coordinates_data(postgres, zones_data)

## entering coordinate data for parking spots

input_spot_coordinates_data(postgres, spots_data)

## entering selected data for parking spots

# input_spots_data(postgres, spots_data)

## bicycle spots table creation

create_bicycle_spots_table(postgres)

## insert data into bicycle spots table

input_bicycle_data(postgres, bicycle_data)

# committing it all to the relational database

postgres.commit()