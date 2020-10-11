from pathlib import Path

from ReaCombiner import db
from ReaCombiner.main import getHome

dbfile = getHome().replace('\\', '/') + '/sqlitedb'
Path(dbfile).touch(exist_ok=True)
db.createConnection(dbfile)
db.dropTables()
db.createTables()
db.close()
