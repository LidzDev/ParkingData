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

postgres_engine = create_engine(postgres_url, echo=True)
postgres = postgres_engine.connect()

# postgres.execute(text("DROP TABLE IF EXISTS hours"))



postgres.commit()

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