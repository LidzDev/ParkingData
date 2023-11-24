import json
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from pymongo import MongoClient


postgres_url = URL.create(
    drivername="postgresql",
    username="darrenlackie",  # change to your own database username
    host="localhost",
    database="parking",
)

zones_path = "./Controlled_Parking_Zones.geojson"
parking_zones = open(zones_path)
zones_data = json.load(parking_zones)
parking_zones.close()

postgres_engine = create_engine(postgres_url, echo=True)
postgres = postgres_engine.connect()

# postgres.execute(text("DROP TABLE IF EXISTS hours"))

# def create_bicycle_spots_table(postgres):
#     bicycle_spots_table = """
#         CREATE TABLE bicycle_spots (
#         id SERIAL PRIMARY KEY,
#         council_identifier VARCHAR(50),
#         capacity VARCHAR(10),
#         latitude VARCHAR(20),
#         longitude VARCHAR(20)
#         )
# """
#     postgres.execute(text(bicycle_spots_table))


def insert_polygon_coordinates_data(postgres, zones_data):
    for feature in zones_data['features']:
        zone_no = feature['properties']['cacz_ref_n']
        outer_list = feature['geometry']['coordinates']
        type = feature['geometry']['type']
        if type == "MultiPolygon":
            for inner_list in outer_list:
                for geo_points_list in inner_list:
                    for coordinates in geo_points_list:
                        longitude = coordinates[0]
                        latitude = coordinates[1]                      
        else:
            for inner_list in outer_list:
                for geo_points_list in inner_list:
                    longitude = geo_points_list[0]
                    latitude = geo_points_list[1]

insert_polygon_coordinates_data(postgres, zones_data)





#         values = {
#             'council_identifier' : council_identifier,
#             'capacity' : cap,
#             'longitude' : longitude,
#             'latitude' : latitude
#         }

#         insert_into_bicycle_table = text ("""
#             INSERT INTO bicycle_spots (
#             council_identifier,
#             capacity,
#             longitude,
#             latitude)
#             VALUES (
#             :council_identifier,
#             :capacity,
#             :longitude,
#             :latitude)
#         """)
#         postgres.execute(insert_into_bicycle_table, values)

# postgres.commit()

# for feature in zones_data['features']:
#         zone_no = feature['properties']['cacz_ref_n']
#         if zone_no == "5A":
#             outer_list = feature['geometry']['coordinates']
#             for inner_list in outer_list:
#                 for geo_points_list in inner_list:
#                     print("{"f" latitude: {geo_points_list[1]}, longitude: {geo_points_list[0]} ""},")
#         else:
#             continue

# def add_price_data(postgres):

#     for identifier in price_data:
                
#                 values = {
#                 'price' : identifier['price'],
#                 'council_zone_identifier' : identifier['council_zone_identifier']
#                 }

#                 add_price_data = text("""
#                     UPDATE parking_zones SET price = :price 
#                     WHERE council_zone_identifier = :council_zone_identifier
#                 """)
#                 postgres.execute(add_price_data, values)

# add_price_data(postgres)