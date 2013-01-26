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

		fieldtypes = guess_datatypes(r)

		f.seek(0)
		if has_header:
			r.next()

		# connect to database
		with sqlite3.connect(dbpath) as conn:
			conn.text_factory = str
			c = conn.cursor()

			# conditional create
			sql_create = 'CREATE TABLE IF NOT EXISTS `%s` (%s);' % (table, ','.join(['`%s` %s' % (n, t) for (n, t) in zip(fieldnames, fieldtypes)]))
			c.execute(sql_create)

			# insert csv values
			sql_insert = 'INSERT INTO `%s` VALUES (%s);' % (table, ','.join(['?']*len(fieldnames)))
			for row in r:
				c.execute(sql_insert, row)

def guess_datatypes(csvreader, max=100):
	types = []
	for i, row in enumerate(csvreader):
		if len(types) == 0:
			types.extend([None] * len(row))
		if i >= max:
			break
		for j, cell in enumerate(row):
			if types[j] == None:
				for type_try in [long, float]:
					try:
						type_try(cell)
						types[j] = type_try
						break
					except:
						pass
			elif types[j] in [long, float]:
				try:
					types[j](cell)
				except:
					types[j] = str

	conversion = {long:"INTEGER",float:"REAL",str:"TEXT",None:"TEXT"}
	
	return [conversion[x] for x in types]


if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print('''csv2sqlite3.py CSV_FILE [ DB_FILE [ TABLE_NAME ] ]''')
	else:
		convert(*sys.argv[1:])
