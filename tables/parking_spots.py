from sqlalchemy import text

def create_parking_spots_table(postgres):
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