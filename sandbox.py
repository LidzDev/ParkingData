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

spots_path = "./Parking_bays.geojson"
parking_spots = open(spots_path)
spots_data = json.load(parking_spots)
parking_spots.close()

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


def input_spot_coordinates_data(postgres, spots_data):
    for feature in spots_data['features']:
        council_bay_identifier = feature['properties']['id']
        print(council_bay_identifier)
        outer_list = feature['geometry']['coordinates']
        type = feature['geometry']['type']
        if type == "MultiPolygon":
            for inner_list in outer_list:
                for geo_points_list in inner_list:
                    for coordinates in geo_points_list:
                        longitude = coordinates[0]
                        latitude = coordinates[1]
                        
                        values = {
                        'council_bay_identifier' : council_bay_identifier,
                        'longitude' : longitude,
                        'latitude' : latitude,
                        }

                        spot_coordinates_insert = text("""
                        INSERT INTO spot_coordinates (
                            parking_spots_id,
                            longitude,
                            latitude)
                        VALUES (
                            (SELECT id FROM parking_spots WHERE council_bay_identifier = :council_bay_identifier)
                            :longitude,
                            :latitude)
                        """)
                        postgres.execute(spot_coordinates_insert, values)

        else:
            for inner_list in outer_list:
                for geo_points_list in inner_list:
                    values = {
                        'council_bay_identifier' : council_bay_identifier,
                        'longitude' : geo_points_list[0],
                        'latitude' : geo_points_list[1],
                    }

input_spot_coordinates_data(postgres, spots_data)



def set_spot_coordinate_values(postgres, values):
    spot_coordinates_insert = text("""
        INSERT INTO spot_coordinates (
            parking_spots_id,
            longitude,
            latitude)
        VALUES (
            (SELECT id FROM parking_spots WHERE council_bay_identifier = :council_bay_identifier)
            :longitude,
            :latitude)
        """)
    postgres.execute(spot_coordinates_insert, values)