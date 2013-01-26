csv2sqlite3
===========

convert a csv file to a sqlite3 database using python's csv "sniffer" heuristics

Usage
-----

`csv2sqlite3.py CSV_FILE [ DB_FILE [ TABLE_NAME ] ]`

Example
-----

    $ echo "id,name,age
    > 1,Alice,30
    > 2,Bob,35" > test.csv
    $
    $ ./csv2sqlite3.py test.csv
    $
    $ sqlite3 test.db "SELECT name, age FROM test;"
    Alice|30
    Bob|35
