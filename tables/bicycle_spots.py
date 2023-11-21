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

        values = {
            'council_identifier' : council_identifier,
            'capacity' : cap 
        }

        insert_into_bicycle_table = text ("""
            INSERT INTO bicycle_spots (
            council_identifier,
            capacity)
            VALUES (
            :council_identifier,
            :capacity)
        """)
        postgres.execute(insert_into_bicycle_table, values)
    

