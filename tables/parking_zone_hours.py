from sqlalchemy import text

def create_parking_zone_hours_table(postgres):
    parking_zone_hours_table = """
    CREATE TABLE parking_zone_hours (
    id SERIAL PRIMARY KEY,
    parking_zones_id INTEGER REFERENCES parking_zones(id),
    hours_id INTEGER REFERENCES hours(id)
    )
"""
    postgres.execute(text(parking_zone_hours_table))

def insert_parking_zone_hours_data(postgres):
    parking_zone_hours_mapping = {
    1: [2, 4, 6, 8, 10],
    2: [2, 4, 6, 8, 10],
    3: [1, 3, 5, 7, 9, 11, 12],
    4: [1, 3, 5, 7, 9, 11, 12],
    5: [1, 3, 5, 7, 9, 11, 12],
    6: [1, 3, 5, 7, 9, 11, 12],
    7: [1, 3, 5, 7, 9, 11, 12],
    8: [2, 4, 6, 8, 10],
    9: [2, 4, 6, 8, 10],
    10: [2, 4, 6, 8, 10],
    11: [2, 4, 6, 8, 10],
    12: [2, 4, 6, 8, 10],
    13: [2, 4, 6, 8, 10],
    14: [2, 4, 6, 8, 10],
    15: [2, 4, 6, 8, 10],
    16: [2, 4, 6, 8, 10],
    17: [2, 4, 6, 8, 10],
    18: [2, 4, 6, 8, 10],
    19: [2, 4, 6, 8, 10]
}

    for parking_zones_id, hours_ids in parking_zone_hours_mapping.items():
        for hours_id in hours_ids:
            parking_zone_hours_insert = text("""
                INSERT INTO parking_zone_hours (parking_zones_id, hours_id)
                VALUES (:parking_zones_id, :hours_id)
            """)
            postgres.execute(parking_zone_hours_insert, {'parking_zones_id': parking_zones_id, 'hours_id': hours_id})