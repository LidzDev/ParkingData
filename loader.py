from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import json
from pymongo import MongoClient

# consider holding the filepaths and collection names  in a hashmap



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

collection_bicycle_spots = json_db['bicyle_spots']
collection_bicycle_spots.drop()
collection_bicycle_spots.insert_one(bicycle_data)
bicycle_spots.close()

postgres_url = URL.create(
    drivername = "postgresql", 
    username = "Lydia",  # change to your own database username
    host = "localhost",
    database = "parking"
)

# swap between the following two lines if you want to see more or less output from the postgres sql commands
postgres_engine = create_engine(postgres_url, echo=True)
#postgres_engine = create_engine(postgres_url)
postgres = postgres_engine.connect()

# NB comment the following block out for first run
postgres.execute(text("DROP TABLE parking_spots"))
postgres.execute(text("DROP TABLE parking_zones"))
postgres.execute(text("DROP TABLE hours"))
postgres.execute(text("DROP TABLE coordinates"))
postgres.execute(text("DROP TABLE vehicles"))
# end block

## vehicle table creation

vehicles_table = """
    CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
    )
"""
postgres.execute(text(vehicles_table))

## vehicle types loaded here - add here if we need more

vehicle_table_data = [
    {"name": "car"},
    {"name": "bike"}
]

postgres.execute(
    text("INSERT INTO vehicles (name) VALUES (:name)"),
    vehicle_table_data
)

## hours table creation

hours_table = """
    CREATE TABLE hours (
    id SERIAL PRIMARY KEY, 
    start_hours VARCHAR(10),
    end_hours VARCHAR(10)
    )
"""
postgres.execute(text(hours_table))

## parking zones table creation

parking_zones_table = """
    CREATE TABLE parking_zones (
    id SERIAL PRIMARY KEY,
    council_zone_identifier VARCHAR(10) NOT NULL,
    price INTEGER,
    hours_id INTEGER REFERENCES hours(id),
    description VARCHAR(250),
    public_spaces INTEGER, 
    permit_spaces INTEGER,
    off_street_spaces INTEGER
    )
"""
postgres.execute(text(parking_zones_table))

## coordinates table creation

coordinates_table = """
    CREATE TABLE coordinates (
    id SERIAL PRIMARY KEY,
    latitude VARCHAR(20),
    longitude VARCHAR(20),
    latitudeDelta VARCHAR(20),
    longitudeDelta VARCHAR(20)
    )
"""
postgres.execute(text(coordinates_table))

# parking spots table creation

parking_spots_table = """
    CREATE TABLE parking_spots (
        id SERIAL PRIMARY KEY,
        vehicle_id INTEGER REFERENCES vehicles NOT NULL,
        coordinates_id INTEGER REFERENCES coordinates(id) NOT NULL,
        address VARCHAR(250),
        parking_zone_id INTEGER REFERENCES parking_zones(id),
        parking_info VARCHAR(300),
        bay_type VARCHAR(100),
        council_bay_identifier VARCHAR(20)
    )
"""
postgres.execute(text(parking_spots_table))

## Selected Parking zone Data read in from json

for feature in zones_data['features']:

    values = {
            'council_zone' : feature['properties']['cacz_ref_n'],
            'description' : feature['properties']['Type'],
            'public_spaces' : feature['properties']['no_pub_spa'],
            'permit_spaces' : feature['properties']['no_res_spa'],
            'off_street_spaces' : feature['properties']['no_osp_spa']
    }

    parking_zone_insert = text("""
        INSERT INTO parking_zones (
            council_zone_identifier, 
            description, 
            public_spaces, 
            permit_spaces, 
            off_street_spaces) 
        VALUES (
            :council_zone, 
            :description, 
            :public_spaces, 
            :permit_spaces, 
            :off_street_spaces)
""")
    postgres.execute(parking_zone_insert, values)

# ## Selected Parking spots Data read in from json

# for feature in spots_data['features']:

#     values = {
#             'council_zone_id' : feature['properties']['Zone_No'],
#             'bay_type' : feature['properties']['Bay_Type'],
#             'bay_id' : feature['properties']['id']
#     }
# # todo need to retrieve correct parking zone id

#     parking_spots_insert = text("""
#         INSERT INTO parking_spots (
#             council_zone_identifier, 
#             bay_type, 
#             council_bay_identifier 
# ) 
#         VALUES (
#             :council_zone, 
#             :bay_type, 
#             :council_bay_identifier )
# """)
#     postgres.execute(parking_spots_insert, values)




# committing it all to the relational database

postgres.commit()
