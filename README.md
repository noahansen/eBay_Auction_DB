# eBay Auction DataBase

## Purpose
To apply the principles of database design to implement a good relational schema.

## Data
The data comes from eBay's website, representing a single point in time: December 20th, 2001, 00:00:01

## This project consists of 4 parts: 
- Designing the relational schema
- Parsing the JSON data into a format that fits the designed schema
- Loading the data into SQLite
- Testing the model with queries

## Execution
1. sh runParser.sh
2. sqlite3 <db_name> < create.sql
3. sqlite3 <db_name> < load.txt
4. sqlite3 <db_name> < query*.sql

## Notes
- RunParser.sh calls the parser on each JSON file in /ebay_data/. It then removes duplicate rows in all of the resulting .dat files, as some duplicates are created during parsing.
- load.txt loads the output files from the parser into the tables of the database.
- Uses Unix commands
