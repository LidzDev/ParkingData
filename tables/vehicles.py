from sqlalchemy import text

def create_vehicles_table(postgres):
    vehicles_table = """
        CREATE TABLE vehicles (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL
        )
    """
    postgres.execute(text(vehicles_table))

## vehicle types loaded here - add here if we need more

    vehicle_table_data = [
        {"name": "car"},
        {"name": "bike"}
    ]

    postgres.execute(text("INSERT INTO vehicles (name) VALUES (:name)"), vehicle_table_data)