from pathlib import Path
from sys import path

import db
from main import getHome

dbfile = getHome().replace('\\', '/') + '/sqlitedb'
Path(dbfile).touch(exist_ok=True)
db.createConnection(dbfile)
db.dropTables()
db.createTables()
db.close()
