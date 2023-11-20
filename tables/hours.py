from sqlalchemy import text

def create_hours_table(postgres):
    hours_table = """
        CREATE TABLE hours (
        id SERIAL PRIMARY KEY, 
        day_of_week VARCHAR(10),
        start_hours VARCHAR(10),
        end_hours VARCHAR(10)
        )
    """
    postgres.execute(text(hours_table))

    hours_data = [
        {"day_of_week": "Monday", "start_hours": "08:30", "end_hours": "18:30"},
        {"day_of_week": "Monday", "start_hours": "08:30", "end_hours": "17:30"},
        {"day_of_week": "Tuesday", "start_hours": "08:30", "end_hours": "18:30"},
        {"day_of_week": "Tuesday", "start_hours": "08:30", "end_hours": "17:30"},
        {"day_of_week": "Wednesday", "start_hours": "08:30", "end_hours": "18:30"},
        {"day_of_week": "Wednesday", "start_hours": "08:30", "end_hours": "17:30"},
        {"day_of_week": "Thursday", "start_hours": "08:30", "end_hours": "18:30"},
        {"day_of_week": "Thursday", "start_hours": "08:30", "end_hours": "17:30"},
        {"day_of_week": "Friday", "start_hours": "08:30", "end_hours": "18:30"},
        {"day_of_week": "Friday", "start_hours": "08:30", "end_hours": "17:30"},
        {"day_of_week": "Saturday", "start_hours": "08:30", "end_hours": "18:30"},
        {"day_of_week": "Sunday", "start_hours": "12:30", "end_hours": "17:30"},
    ]

    hours_insert = text("""
            INSERT INTO hours (
                day_of_week,
                start_hours,
                end_hours)
            VALUES (
                :day_of_week,
                :start_hours,
                :end_hours)
            """)

    postgres.execute(hours_insert, hours_data)