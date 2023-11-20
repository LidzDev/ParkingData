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

# NB comment the following block out for first run
postgres.execute(text("DROP TABLE parking_spots"))
postgres.execute(text("DROP TABLE parking_zone_hours"))
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
    day_of_week VARCHAR(10),
    start_hours VARCHAR(10),
    end_hours VARCHAR(10)
    )
"""
postgres.execute(text(hours_table))

hours_data = [
    {"day_of_week" : "Monday", "start_hours" : "08:30", "end_hours" : "18:30"},
    {"day_of_week" : "Monday", "start_hours" : "08:30", "end_hours" : "17:30"},
    {"day_of_week" : "Tuesday", "start_hours" : "08:30", "end_hours" : "18:30"},
    {"day_of_week" : "Tuesday", "start_hours" : "08:30", "end_hours" : "17:30"},
    {"day_of_week" : "Wednesday", "start_hours" : "08:30", "end_hours" : "18:30"},
    {"day_of_week" : "Wednesday", "start_hours" : "08:30", "end_hours" : "17:30"},
    {"day_of_week" : "Thursday", "start_hours" : "08:30", "end_hours" : "18:30"},
    {"day_of_week" : "Thursday", "start_hours" : "08:30", "end_hours" : "17:30"},
    {"day_of_week" : "Friday", "start_hours" : "08:30", "end_hours" : "18:30"},
    {"day_of_week" : "Friday", "start_hours" : "08:30", "end_hours" : "17:30"},
    {"day_of_week" : "Saturday", "start_hours" : "08:30", "end_hours" : "18:30"},
    {"day_of_week" : "Sunday", "start_hours" : "12:30", "end_hours" : "17:30"},
    
]

hours_insert = text ("""
        INSERT INTO hours (
            day_of_week,
            start_hours,
            end_hours)
        VALUES (
            :day_of_week,
            :start_hours,
            :end_hours)
        """)

postgres.execute(hours_insert, hours_data)

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

parking_zone_hours_table = """
    CREATE TABLE parking_zone_hours (
    id SERIAL PRIMARY KEY,
    parking_zones_id INTEGER REFERENCES parking_zones(id),
    hours_id INTEGER REFERENCES hours(id)
    )
"""
postgres.execute(text(parking_zone_hours_table))

## coordinates table creation

coordinates_table = """
    CREATE TABLE coordinates (
    id SERIAL PRIMARY KEY,
    council_zone_identifier VARCHAR(10),
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

# for feature in zones_data['features']:

#     price_data = [
#         {'council_zone_identifier' : '1', 'price' : '3.90'},
#         {'council_zone_identifier' : '1A', 'price' : '6.70'},
#         {'council_zone_identifier' : '2', 'price' : '6.70'},
#         {'council_zone_identifier' : '3', 'price' : '3.90'},
#         {'council_zone_identifier' : '4', 'price' : '3.90'},
#         {'council_zone_identifier' : '5', 'price' : '4.60'},
#         {'council_zone_identifier' : '5A', 'price' : '4.60'},
#         {'council_zone_identifier' : '6', 'price' : '4.60'},
#         {'council_zone_identifier' : '7', 'price' : '3.90'},
#         {'council_zone_identifier' : '8', 'price' : '2.50'},
#         {'council_zone_identifier' : 'N1', 'price' : '2.50'},
#         {'council_zone_identifier' : 'N2', 'price' : '2.50'},
#         {'council_zone_identifier' : 'N3', 'price' : '2.50'},
#         {'council_zone_identifier' : 'N4', 'price' : '2.50'},
#         {'council_zone_identifier' : 'N5', 'price' : '2.50'},
#         {'council_zone_identifier' : 'S1', 'price' : '2.50'},
#         {'council_zone_identifier' : 'S2', 'price' : '2.50'},
#         {'council_zone_identifier' : 'S3', 'price' : '2.50'},
#         {'council_zone_identifier' : 'S4', 'price' : '2.50'}
#     ]

    # parking_zones_price_insert = text(
    #     INSERT INTO parking_zones (
    #         council_
    #     )
    # )

parking_zone_hours_mapping = {
    1: [2, 4, 6, 8, 10],
    2: [2, 4, 6, 8, 10],
    3: [1, 3, 5, 7, 9, 11, 12],
    4: [1, 3, 5, 7, 9, 11, 12],
    5: [1, 3, 5, 7, 9, 11, 12],
    6: [1, 3, 5, 7, 9, 11, 12],
    7: [1, 3, 5, 7, 9, 11, 12],
    8: [2, 4, 6, 8, 10],
    9: [2, 4, 6, 8, 10],
    10: [2, 4, 6, 8, 10],
    11: [2, 4, 6, 8, 10],
    12: [2, 4, 6, 8, 10],
    13: [2, 4, 6, 8, 10],
    14: [2, 4, 6, 8, 10],
    15: [2, 4, 6, 8, 10],
    16: [2, 4, 6, 8, 10],
    17: [2, 4, 6, 8, 10],
    18: [2, 4, 6, 8, 10],
    19: [2, 4, 6, 8, 10]
}

for parking_zones_id, hours_ids in parking_zone_hours_mapping.items():
    for hours_id in hours_ids:
        parking_zone_hours_insert = text("""
            INSERT INTO parking_zone_hours (parking_zones_id, hours_id)
            VALUES (:parking_zones_id, :hours_id)
        """)
        postgres.execute(parking_zone_hours_insert, {'parking_zones_id': parking_zones_id, 'hours_id': hours_id})

## entering coordinate data for parking zone polygons

for feature in zones_data['features']:
    zone_no = feature['properties']['cacz_ref_n']
    outer_list = feature['geometry']['coordinates']
    for inner_list in outer_list:
        for geo_points_list in inner_list:
            values = {
                'longitude' : geo_points_list[0],
                'latitude' : geo_points_list[1],
                'council_zone' : zone_no
            }

            coordinates_insert = text("""
                INSERT INTO coordinates (
                    longitude,
                    latitude,
                    council_zone_identifier)
                VALUES (
                    :longitude,
                    :latitude,
                    :council_zone)
            """)
            postgres.execute(coordinates_insert, values)

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
#             :council_zone_id, 
#             :bay_type, 
#             :council_bay_identifier )
# """)
#     postgres.execute(parking_spots_insert, values)




# committing it all to the relational database

postgres.commit()
