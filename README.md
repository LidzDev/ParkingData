# Parking Data

## Summary
Python Application to process data from publicly available APIs for use by the SmartPark app.

## Project Information
For more information on the overall project please see the [overview](https://github.com/cemmartin/SmartPark/README.md).

## Description
For the current version of the application we download the data from the Edinburgh City Council and Open Street APIs. As we start processing we save copies of the json in the MongoDB, and then we iterate over the data to generate the relational database. After this has done we run a post processing script to prepare the data for use by the app.

## Prerequisites
To be able to run the ParkingData application on your machine you need to have the following already installed:
- Python 3.11 
- SQLAlchemy 2.0.20
- PyMongo 4.6.0
- MongoDB 6.0.10 Community
- PostgresQL 14.10

## Installation Notes
1.  Make sure you are in the directory that you have created for the project. 
    `cd SmartPark`
2. Download the repository
    `git clone git@github.com:LidzDev/ParkingData.git`
3. Create the parking database. 
    `createdb parking`
4. Change line 16 in loader.py to be your postgres database username
    `username = "lydia",  # change this value`
5. Run the loader script and wait until it tells you it has finished
    `python3 loader.py`
6. Change line 12 in post_processing.py to be your postgres database username as well
7. Run the post_processing.py and check that it tells you it is finished
    `python3 post_processing.py`

## Future Development
We'd like to replace the manual data fetch by an automated fetch and also do some web scraping for more data.


