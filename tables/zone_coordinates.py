from sqlalchemy import text

def create_zone_coordinates_table(postgres):
    zone_coordinates_table = """
    CREATE TABLE zone_coordinates (
    id SERIAL PRIMARY KEY,
    zone_id INTEGER REFERENCES parking_zones(id),
    latitude VARCHAR(20),
    longitude VARCHAR(20),
    latitudeDelta VARCHAR(20),
    longitudeDelta VARCHAR(20)
    )
"""
    postgres.execute(text(zone_coordinates_table))   


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
                        
                        values = {
                        'longitude' : longitude,
                        'latitude' : latitude,
                        'council_zone_identifier' : zone_no 
                        }
                        set_coordinate_values(postgres, values)
        else:
            for inner_list in outer_list:
                for geo_points_list in inner_list:
                    longitude = geo_points_list[0]
                    latitude = geo_points_list[1]

                    values = {
                        'longitude' : longitude,
                        'latitude' : latitude,
                        'council_zone_identifier' : zone_no 
                    }
                    set_coordinate_values(postgres, values)

def set_coordinate_values(postgres, values):
    zone_coordinates_insert = text("""
    INSERT INTO zone_coordinates (
        longitude,
        latitude,
        zone_id)
    VALUES (
        :longitude,
        :latitude,
        (SELECT id FROM parking_zones WHERE council_zone_identifier = :council_zone_identifier))
    """)
    postgres.execute(zone_coordinates_insert, values)