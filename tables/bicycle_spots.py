from sqlalchemy import text

def create_bicycle_spots_table(postgres):
    bicycle_spots_table = """
        CREATE TABLE bicycle_spots (
        id SERIAL PRIMARY KEY,
        council_identifier VARCHAR(50),
        capacity VARCHAR(10),
        latitude VARCHAR(20),
        longitude VARCHAR(20)
        )
"""
    postgres.execute(text(bicycle_spots_table))


def input_bicycle_data(postgres, bicycle_data):
    for feature in bicycle_data['features']:
        council_identifier = feature['properties'].get('@id', "No data")
        cap = feature['properties'].get('capacity')
        if cap is None:
            cap = "No data"
        outer_list = feature['geometry']['coordinates']    
        type = feature['geometry']['type']

# only pulling the first coordinates of each entry out
        if type == "LineString":
            longitude = outer_list[0][0]
            latitude = outer_list[0][1]
            
            values = {
            'council_identifier' : council_identifier,
            'capacity' : cap,
            'longitude' : longitude,
            'latitude' : latitude
            }
            set_coordinate_values(postgres, values)
        
        elif type == "Point":
            longitude = outer_list[0]
            latitude = outer_list[1]
            
            values = {
            'council_identifier' : council_identifier,
            'capacity' : cap,
            'longitude' : longitude,
            'latitude' : latitude
            }
            set_coordinate_values(postgres, values)
        
        else:
            for geo_points_list in outer_list:
                    longitude = geo_points_list[0][0]
                    latitude = geo_points_list[0][1]
                    
                    values = {
                        'council_identifier' : council_identifier,
                        'capacity' : cap,
                        'longitude' : longitude,
                        'latitude' : latitude
                    }
                    set_coordinate_values(postgres, values)



def set_coordinate_values(postgres, values):
    insert_into_bicycle_table = text ("""
    INSERT INTO bicycle_spots (
    council_identifier,
    capacity,
    longitude,
    latitude)
    VALUES (
    :council_identifier,
    :capacity,
    :longitude,
    :latitude)
""")
    postgres.execute(insert_into_bicycle_table, values)

