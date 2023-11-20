from sqlalchemy import text

def create_coordinates_table(postgres):
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


def insert_polygon_coordinates_data(postgres, zones_data):
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