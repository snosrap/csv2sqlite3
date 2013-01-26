#!/usr/bin/python

import os, sys
import csv, sqlite3

def convert(csvpath, dbpath=None, table=None):

	# file.csv -> file.db
	if not dbpath:
		dbpath = '%s.db' % os.path.splitext(csvpath)[0]

	# /path/file.csv -> file
	if not table:
		table = os.path.basename(os.path.splitext(csvpath)[0])

	with open(csvpath, 'rb') as f:
		
		# sample the data, then rewind
		sample = f.read(1024)
		f.seek(0)

		# sniff the sample data to guess the delimeters, etc
		dialect = csv.Sniffer().sniff(sample)
		has_header = csv.Sniffer().has_header(sample)

		# column names are either in the first (header) row or c0, c1, c2 if there is not header row
		fieldnames = [x if has_header else 'c%s'%i for i,x in enumerate(csv.reader(f, dialect=dialect).next())]
		f.seek(0)

		# prepare the reader and skip the header row
		r = csv.reader(f, dialect=dialect)
		if has_header:
			r.next()

		# connect to database
		with sqlite3.connect(dbpath) as conn:
			c = conn.cursor()

			# conditional create
			sql_create = 'CREATE TABLE IF NOT EXISTS `%s` (%s);' % (table, ','.join(fieldnames))
			c.execute(sql_create)

			# insert csv values
			sql_insert = 'INSERT INTO `%s` VALUES (%s);' % (table, ','.join(['?']*len(fieldnames)))
			for row in r:
				c.execute(sql_insert, row)

if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print('''csv2sqlite3.py CSV_FILE [ DB_FILE [ TABLE_NAME ] ]''')
	else:
		convert(*sys.argv[1:])
