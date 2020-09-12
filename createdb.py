import db

db.createConnection('/home/roger/sqlitedb')
db.dropTables()
db.createTables()
db.close()
