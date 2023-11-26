import json
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from pymongo import MongoClient

postgres_url = URL.create(
    drivername="postgresql",
    username="user",  # change to your own database username
    host="localhost",
    database="parking",
)

postgres_engine = create_engine(postgres_url, echo=True)
postgres = postgres_engine.connect()

postgres.execute(text("DROP TABLE IF EXISTS hours"))

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