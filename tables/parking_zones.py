from sqlalchemy import text

def create_parking_zones_table(postgres):
    parking_zones_table = """
    CREATE TABLE parking_zones (
    id SERIAL PRIMARY KEY,
    council_zone_identifier VARCHAR(10) NOT NULL,
    price INTEGER,
    hours_id INTEGER REFERENCES hours(id),
    description VARCHAR(250),
    public_spaces INTEGER, 
    permit_spaces INTEGER,
    off_street_spaces INTEGER
    )
"""
    postgres.execute(text(parking_zones_table))


def add_parking_zones_data(postgres, zones_data):
    for feature in zones_data['features']:

        values = {
                'council_zone' : feature['properties']['cacz_ref_n'],
                'description' : feature['properties']['Type'],
                'public_spaces' : feature['properties']['no_pub_spa'],
                'permit_spaces' : feature['properties']['no_res_spa'],
                'off_street_spaces' : feature['properties']['no_osp_spa']
        }

        parking_zone_insert = text("""
            INSERT INTO parking_zones (
                council_zone_identifier, 
                description, 
                public_spaces, 
                permit_spaces, 
                off_street_spaces) 
            VALUES (
                :council_zone, 
                :description, 
                :public_spaces, 
                :permit_spaces, 
                :off_street_spaces)
            """)
        postgres.execute(parking_zone_insert, values)

## BLOCKER - need to work out how to insert the following price data

# for feature in zones_data['features']:

#     price_data = [
#         {'council_zone_identifier' : '1', 'price' : '3.90'},
#         {'council_zone_identifier' : '1A', 'price' : '6.70'},
#         {'council_zone_identifier' : '2', 'price' : '6.70'},
#         {'council_zone_identifier' : '3', 'price' : '3.90'},
#         {'council_zone_identifier' : '4', 'price' : '3.90'},
#         {'council_zone_identifier' : '5', 'price' : '4.60'},
#         {'council_zone_identifier' : '5A', 'price' : '4.60'},
#         {'council_zone_identifier' : '6', 'price' : '4.60'},
#         {'council_zone_identifier' : '7', 'price' : '3.90'},
#         {'council_zone_identifier' : '8', 'price' : '2.50'},
#         {'council_zone_identifier' : 'N1', 'price' : '2.50'},
#         {'council_zone_identifier' : 'N2', 'price' : '2.50'},
#         {'council_zone_identifier' : 'N3', 'price' : '2.50'},
#         {'council_zone_identifier' : 'N4', 'price' : '2.50'},
#         {'council_zone_identifier' : 'N5', 'price' : '2.50'},
#         {'council_zone_identifier' : 'S1', 'price' : '2.50'},
#         {'council_zone_identifier' : 'S2', 'price' : '2.50'},
#         {'council_zone_identifier' : 'S3', 'price' : '2.50'},
#         {'council_zone_identifier' : 'S4', 'price' : '2.50'}
#     ]

    # parking_zones_price_insert = text(
    #     INSERT INTO parking_zones (
    #         council_
    #     )
    # )