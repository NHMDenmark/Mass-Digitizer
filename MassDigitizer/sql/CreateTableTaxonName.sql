CREATE TABLE "taxonname" (
	"id"	INTEGER NOT NULL UNIQUE,
	"taxonid"	INTEGER,
	"name"	TEXT,
	"fullname"	TEXT,
	"rankid"	INTEGER,
	"classid"	INTEGER,
	"treedefid"	INTEGER,
	"parentfullname"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)