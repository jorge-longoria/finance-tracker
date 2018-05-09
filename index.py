#!/usr/bin/python

import cgi
import psycopg2 as pg
from psycopg2 import sql

DB_NAME='finance_tracker'
DB_USER='postgres'
DB_PASS='postgres'

#Get HTTP parameters.
ARGS = cgi.FieldStorage()

args = {}

#Amount
if 'amount' in ARGS:
    args['amount'] = ARGS['amount'].value
else:
    args['amount'] = 'UNKNOWN'

#Vendor
if 'vendor' in ARGS:
    args['vendor'] = ARGS['vendor'].value
else:
    args['vendor'] = 'UNKNOWN'

#Category
if 'category' in ARGS:
    args['category'] = ARGS['category'].value
else:
    args['category'] = 'UNKNOWN'

#Date
if 'date' in ARGS:
    args['date'] = ARGS['date'].value
else:
    args['date'] = 'UNKNOWN'

#Entry Type
if 'entry_type' in ARGS:
    args['entry_type'] = ARGS['entry_type'].value
else:
    args['entry_type'] = 'UNKNOWN'




#Open the connection.
conn = pg.connect('dbname={0} user={1} password={2}'.format(DB_NAME, DB_USER, DB_PASS))

#Open a cursor.
cur = conn.cursor()

if args['entry_type'] != 'UNKNOWN':
    #Read query file.
    newTransaction = sql.SQL(open('sql/add-transaction.sql', 'r').read()).format(sql.Literal(args['entry_type']), sql.Literal(args['category']), sql.Literal(args['date']), sql.Literal(args['amount']), sql.Literal(args['vendor']))

    #Execute the insert.
    cur.execute(newTransaction)


#Print HTML headers and content.
print 'Content-Type: text/html\n'

page_body = open('html/index.html', 'r').read()

print page_body


#Commit transactions and clean up.
conn.commit()

cur.close()
conn.close()
