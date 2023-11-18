from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

url = URL.create(
    drivername = "postgresql", 
    username = "Lydia",  # change to your own database username
    host = "localhost",
    database = "parking"
)
engine = create_engine(url, echo=True)

connection = engine.connect()
    # result = connection.execute(text("select 'hello world'"))
    # print(result.all())

# comment the following block out for first run
connection.execute(text("DROP TABLE parking_spots"))
connection.execute(text("DROP TABLE parking_zones"))
connection.execute(text("DROP TABLE hours"))
connection.execute(text("DROP TABLE coordinates"))
connection.execute(text("DROP TABLE vehicles"))
# end block

connection.execute(text("CREATE TABLE vehicles (id SERIAL PRIMARY KEY, name VARCHAR(100) NOT NULL)"))
# vehicle types loaded here - add here if we need more
connection.execute(
        text("INSERT INTO vehicles (name) VALUES (:name)"),
        [{"name": "car"},{"name": "bicyle"}]
    )
connection.execute(text("CREATE TABLE hours (id SERIAL PRIMARY KEY, start_hours VARCHAR(10), end_hours VARCHAR(10))"))
connection.execute(text("CREATE TABLE parking_zones (id SERIAL PRIMARY KEY, council_zone_identifier VARCHAR(10) NOT NULL, price INTEGER, hours_id INTEGER REFERENCES hours(id), description VARCHAR(250), public_spaces INTEGER, permit_spaces INTEGER, disabled_spaces INTEGER )"))
connection.execute(text("CREATE TABLE coordinates (id SERIAL PRIMARY KEY, latitude VARCHAR(20), longitude VARCHAR(20), latitude_delta VARCHAR(20), longitude_delta VARCHAR(20))"))
connection.execute(text("CREATE TABLE parking_spots (id SERIAL PRIMARY KEY, vehicle_id INTEGER REFERENCES vehicles NOT NULL, coordinates_id INTEGER REFERENCES coordinates(id) NOT NULL, address VARCHAR(250), parking_zone_id INTEGER REFERENCES parking_zones(id), parking_info VARCHAR(300), bay_type VARCHAR(100), council_bay_identifier VARCHAR(20))"))

connection.commit()
