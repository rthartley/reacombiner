import db
from main import getHome

db.createConnection(getHome().replace('\\', '/') + '/sqlitedb')
db.dropTables()
db.createTables()
db.close()
