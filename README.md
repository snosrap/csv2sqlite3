csv2sqlite3
===========

convert a csv file to a sqlite3 database using python's csv "sniffer" heuristics

Usage
-----

    usage: csv2sqlite3.py [-h] [-d DB_FILE] [-t TABLE_NAME] [-s SQL_CREATE]
                          [-z SAMPLE_SIZE]
                          csv_file
    
    Converts a CSV file to a SQLite3 database
    
    positional arguments:
      csv_file              path to CSV file
    
    optional arguments:
      -h, --help            show this help message and exit
      -d DB_FILE, --db_file DB_FILE
                            path to SQLite3 database file
      -t TABLE_NAME, --table_name TABLE_NAME
                            name of the table
      -s SQL_CREATE, --sql_create SQL_CREATE
                            path to CREATE TABLE .sql file
      -z SAMPLE_SIZE, --sample_size SAMPLE_SIZE
                            how many rows to search to guess datatypes

Example
-------

    $ echo "id,name,age
    1,Alice,30
    2,Bob,35" > test.csv
    
    $ ./csv2sqlite3.py test.csv
    
    $ sqlite3 test.db ".schema"
    CREATE TABLE `test` (
        `id`	INTEGER,
    	`name`	TEXT,
    	`age`	INTEGER
    );
    
    $ sqlite3 test.db "SELECT name, age FROM test;"
    Alice|30
    Bob|35
