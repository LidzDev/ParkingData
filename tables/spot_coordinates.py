from sqlalchemy import text, Table

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
        council_bay_identifier = feature['properties']['id']
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

                        set_spot_coordinate_values(postgres, values)

        else:
            for inner_list in outer_list:
                for geo_points_list in inner_list:
                    values = {
                        'council_bay_identifier' : council_bay_identifier,
                        'longitude' : geo_points_list[0],
                        'latitude' : geo_points_list[1],
                    }
                    # print(council_bay_identifier)
                    set_spot_coordinate_values(postgres, values)

def set_spot_coordinate_values(postgres, values):
    spot_coordinates_insert = text("""
        INSERT INTO spot_coordinates (
            parking_spots_id,
            longitude,
            latitude)
        VALUES (
            (SELECT id FROM parking_spots WHERE council_bay_identifier = :council_bay_identifier),
            :longitude,
            :latitude)
        """)
    postgres.execute(spot_coordinates_insert, values)

def get_coordinates(postgres, engine, metadata):

    Table(
        'spot_coordinates',
        metadata,
        autoload_with=engine,
        extend_existing=True
    )

    query =  text("""
    SELECT DISTINCT ON (parking_spots_id) * from spot_coordinates ORDER BY parking_spots_id 
    """)
    result = postgres.execute(query)
    result_set = result.fetchall()
    return result_set
