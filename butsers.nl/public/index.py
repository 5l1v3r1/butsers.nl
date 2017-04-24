#!/usr/bin/env python
# 

import cgi
import os, sys


# Configuration
configDict = {
	"debug": False, 
	"libDir": os.path.abspath(os.path.join('..', 'modules')),
	"staticDir": os.path.abspath(os.path.join('..', 'static')),
	"dbFile": os.path.abspath(os.path.join('..', 'database', 'butsers.nl.db')),
	#"modulesEnabled": ["nieuws", "butsmarkt", "tartbak", "meuk", "log"],
	"modulesEnabled": ["nieuws", "meuk", "log"],
	}

sys.path.append(configDict['libDir'])
from butsers import butserver
from butsdb import butsdb

databaseHandler = butsdb.ButsDB(configDict)
databaseHandler.init()

butserHandler = butserver.Butserver(configDict, databaseHandler)
butserHandler.handleRequest(os.environ["REQUEST_URI"], cgi.FieldStorage())

databaseHandler.close()