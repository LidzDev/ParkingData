from sqlalchemy import text

def create_parking_spots_table(postgres):
    parking_spots_table = """
    CREATE TABLE parking_spots (
        id SERIAL PRIMARY KEY,
        vehicle_id INTEGER REFERENCES vehicles NOT NULL,
        parking_zone_id INTEGER REFERENCES parking_zones(id),
        bay_type VARCHAR(100),
        council_bay_identifier VARCHAR(20)
    )
"""
    postgres.execute(text(parking_spots_table))


# ## Selected Parking spots Data read in from json

def input_spots_data(postgres, spots_data):
    for feature in spots_data['features']:

        values = {
                'vehicle_id' : 1,
                'council_zone_identifier' : feature['properties']['Zone_No'],
                'bay_type' : feature['properties']['Bay_Type'],
                'council_bay_identifier' : feature['properties']['id']
        }

        parking_spots_insert = text("""
            INSERT INTO parking_spots (
                vehicle_id,
                parking_zone_id,
                bay_type, 
                council_bay_identifier 
    ) 
            VALUES (
                :vehicle_id,
                (SELECT id FROM parking_zones WHERE council_zone_identifier = :council_zone_identifier),
                :bay_type,
                :council_bay_identifier)
    """)
        postgres.execute(parking_spots_insert, values)