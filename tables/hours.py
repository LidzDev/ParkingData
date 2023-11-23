from sqlalchemy import text

def create_hours_table(postgres):
    hours_table = """
        CREATE TABLE hours (
        id SERIAL PRIMARY KEY,
        mon_start VARCHAR(10),
        mon_end VARCHAR(10),
        tues_start VARCHAR(10),
        tues_end VARCHAR(10),
        wed_start VARCHAR(10),
        wed_end VARCHAR(10),
        thurs_start VARCHAR(10),
        thurs_end VARCHAR(10),
        fri_start VARCHAR(10),
        fri_end VARCHAR(10),
        sat_start VARCHAR(10),
        sat_end VARCHAR(10),
        sun_start VARCHAR(10),
        sun_end VARCHAR(10),
        description VARCHAR(200)
        )
    """
    postgres.execute(text(hours_table))

    hours_data = [
        {
        "mon_start": "08:30", "mon_end": "18:30",
        "tues_start": "08:30", "tues_end": "18:30",
        "wed_start": "08:30", "wed_end": "18:30",
        "thurs_start": "08:30", "thurs_end": "18:30",
        "fri_start": "08:30", "fri_end": "18:30",
        "sat_start": "08:30", "sat_end": "18:30",
        "sun_start": "12:30", "sun_end": "18:30",
        "description" : "Paid or permit parking during these hours. Free outwith these hours"
        },
        {
        "mon_start": "08:30", "mon_end": "17:30",
        "tues_start": "08:30", "tues_end": "17:30",
        "wed_start": "08:30", "wed_end": "17:30",
        "thurs_start": "08:30", "thurs_end": "17:30",
        "fri_start": "08:30", "fri_end": "17:30",
        "sat_start": "None", "sat_end": "None",
        "sun_start": "None", "sun_end": "None",
        "description" : "Paid or permit parking during these hours. Free outwith these hours"
        },
        {
        # restricted to permit holders only between...
        "mon_start": "10:00", "mon_end": "11:30",
        "tues_start": "10:00", "tues_end": "11:30",
        "wed_start": "10:00", "wed_end": "11:30",
        "thurs_start": "10:00", "thurs_end": "11:30",
        "fri_start": "10:00", "fri_end": "11:30",
        "sat_start": "None", "sat_end": "None",
        "sun_start": "None", "sun_end": "None",
        "description" : "Permit holders parking only during these hours. Free outwith"
        },
        {
        # restricted to permit holders only between...
        "mon_start": "13:30", "mon_end": "15:00",
        "tues_start": "13:30", "tues_end": "15:00",
        "wed_start": "13:30", "wed_end": "15:00",
        "thurs_start": "13:30", "thurs_end": "15:00",
        "fri_start": "13:30", "fri_end": "15:00",
        "sat_start": "None", "sat_end": "None",
        "sun_start": "None", "sun_end": "None",
        "description" : "Permit holders parking only during these hours. Free outwith"
        },
        {
        # restricted to permit holders only between...
        "mon_start": "11:30", "mon_end": "13:00",
        "tues_start": "11:30", "tues_end": "13:00",
        "wed_start": "11:30", "wed_end": "13:00",
        "thurs_start": "11:30", "thurs_end": "13:00",
        "fri_start": "11:30", "fri_end": "13:00",
        "sat_start": "None", "sat_end": "None",
        "sun_start": "None", "sun_end": "None",
        "description" : "Permit holders parking only during these hours. Free outwith"
        },
        {
        # restricted to permit holders only between...
        "mon_start": "11:00", "mon_end": "12:30",
        "tues_start": "11:00", "tues_end": "12:30",
        "wed_start": "11:00", "wed_end": "12:30",
        "thurs_start": "11:00", "thurs_end": "12:30",
        "fri_start": "11:00", "fri_end": "12:30",
        "sat_start": "None", "sat_end": "None",
        "sun_start": "None", "sun_end": "None",
        "description" : "Permit holders parking only during these hours. Free outwith"
        },
        {
        # restricted to permit holders only between...
        "mon_start": "09:30", "mon_end": "11:00",
        "tues_start": "09:30", "tues_end": "11:00",
        "wed_start": "09:30", "wed_end": "11:00",
        "thurs_start": "09:30", "thurs_end": "11:00",
        "fri_start": "09:30", "fri_end": "11:00",
        "sat_start": "None", "sat_end": "None",
        "sun_start": "None", "sun_end": "None",
        "description" : "Permit holders parking only during these hours. Free outwith"
        },
        {
        # restricted to permit holders only between...
        "mon_start": "12:30", "mon_end": "14:00",
        "tues_start": "12:30", "tues_end": "14:00",
        "wed_start": "12:30", "wed_end": "14:00",
        "thurs_start": "12:30", "thurs_end": "14:00",
        "fri_start": "12:30", "fri_end": "14:00",
        "sat_start": "None", "sat_end": "None",
        "sun_start": "None", "sun_end": "None",
        "description" : "Permit holders parking only during these hours. Free outwith"
        },

    ]

    hours_insert = text("""
        INSERT INTO hours (
            mon_start,
            mon_end,
            tues_start,
            tues_end,
            wed_start,
            wed_end,
            thurs_start,
            thurs_end,
            fri_start,
            fri_end,
            sat_start,
            sat_end,
            sun_start,
            sun_end,
            description)
        VALUES (
            :mon_start,
            :mon_end,
            :tues_start,
            :tues_end,
            :wed_start,
            :wed_end,
            :thurs_start,
            :thurs_end,
            :fri_start,
            :fri_end,
            :sat_start,
            :sat_end,
            :sun_start,
            :sun_end,
            :description)
        """)
    postgres.execute(hours_insert, hours_data)



# def create_hours_table(postgres):
#     hours_table = """
#         CREATE TABLE hours (
#         id SERIAL PRIMARY KEY, 
#         day_of_week VARCHAR(10),
#         start_hours VARCHAR(10),
#         end_hours VARCHAR(10)
#         )
#     """
#     postgres.execute(text(hours_table))

#     hours_data = [
#         {"day_of_week": "Monday", "start_hours": "08:30", "end_hours": "18:30"},
#         {"day_of_week": "Monday", "start_hours": "08:30", "end_hours": "17:30"},
#         {"day_of_week": "Tuesday", "start_hours": "08:30", "end_hours": "18:30"},
#         {"day_of_week": "Tuesday", "start_hours": "08:30", "end_hours": "17:30"},
#         {"day_of_week": "Wednesday", "start_hours": "08:30", "end_hours": "18:30"},
#         {"day_of_week": "Wednesday", "start_hours": "08:30", "end_hours": "17:30"},
#         {"day_of_week": "Thursday", "start_hours": "08:30", "end_hours": "18:30"},
#         {"day_of_week": "Thursday", "start_hours": "08:30", "end_hours": "17:30"},
#         {"day_of_week": "Friday", "start_hours": "08:30", "end_hours": "18:30"},
#         {"day_of_week": "Friday", "start_hours": "08:30", "end_hours": "17:30"},
#         {"day_of_week": "Saturday", "start_hours": "08:30", "end_hours": "18:30"},
#         {"day_of_week": "Sunday", "start_hours": "12:30", "end_hours": "17:30"},
#     ]

#     hours_insert = text("""
#             INSERT INTO hours (
#                 day_of_week,
#                 start_hours,
#                 end_hours)
#             VALUES (
#                 :day_of_week,
#                 :start_hours,
#                 :end_hours)
#             """)

#     postgres.execute(hours_insert, hours_data)