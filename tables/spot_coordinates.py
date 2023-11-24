from sqlalchemy import text

def create_spot_coordinates_table(postgres):
    spot_coordinates_table = """
        CREATE TABLE spot_coordinates (
        id SERIAL PRIMARY KEY,
        parking_spots_id INTEGER REFERENCES parking_spots(id),
        latitude VARCHAR(20),
        longitude VARCHAR(20)
        )
"""
    postgres.execute(text(spot_coordinates_table))

def input_spot_coordinates_data(postgres, spots_data):
    for feature in spots_data['features']:
        outer_list = feature['geometry']['coordinates']
        for inner_list in outer_list:
            for geo_points_list in inner_list:
                values = {
                    'longitude' : geo_points_list[0],
                    'latitude' : geo_points_list[1],
                }

                spot_coordinates_insert = text("""
                        INSERT INTO spot_coordinates (
                            longitude,
                            latitude)
                        VALUES (
                            :longitude,
                            :latitude)
                """)
                postgres.execute(spot_coordinates_insert, values)

