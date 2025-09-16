BEGIN TRANSACTION;
DROP TABLE IF EXISTS "collection";
CREATE TABLE "collection" (
	"id"	INTEGER NOT NULL UNIQUE,
	"spid"	INTEGER,
	"name"	TEXT NOT NULL,
	"institutionid"	INTEGER,
	"taxontreedefid"	INTEGER,
	"visible"	INTEGER,
	"catalognrlength"	INTEGER,
	"usetaxonnumbers"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "dummyrecord";
CREATE TABLE "dummyrecord" (
	"id"	INTEGER NOT NULL UNIQUE,
	"spid"	INTEGER,
	"name"	TEXT,
	"fullname"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "georegion";
CREATE TABLE "georegion" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"source"	TEXT,
	"collectionid"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "institution";
CREATE TABLE "institution" (
	"id"	INTEGER NOT NULL UNIQUE,
	"code"	TEXT,
	"name"	TEXT,
	"url"	TEXT,
	"visible"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "preptype";
CREATE TABLE "preptype" (
	"id"	INTEGER NOT NULL UNIQUE,
	"spid"	INTEGER,
	"name"	INTEGER,
	"collectionid"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "specimen";
CREATE TABLE "specimen" (
	"id"	INTEGER NOT NULL UNIQUE,
	"spid"	INTEGER,
	"catalognumber"	TEXT,
	"taxonfullname"	TEXT,
	"taxonname"	TEXT,
	"taxonauthor"	TEXT,
	"taxonnameid"	INTEGER,
	"familyname"	TEXT,
	"taxonspid"	INTEGER,
	"taxondasscoid"	TEXT,
	"highertaxonname"	TEXT,
	"rankid"	INTEGER,
	"taxonrankname"	TEXT,
	"taxonnumber"	TEXT,
	"taxonnrsource"	TEXT,
	"typestatusname"	TEXT,
	"typestatusid"	NUMERIC,
	"georegionname"	TEXT,
	"georegionsource"	TEXT,
	"georegionid"	INTEGER,
	"storagefullname"	TEXT,
	"storagename"	TEXT,
	"storageid"	NUMERIC,
	"storagerankname"	TEXT,
	"preptypename"	TEXT,
	"preptypeid"	INTEGER,
	"notes"	TEXT,
	"objectcondition"	TEXT,
	"labelobscured"	INTEGER,
	"specimenobscured"	INTEGER,
	"containername"	TEXT,
	"containertype"	INTEGER,
	"institutionid"	INTEGER,
	"institutionname"	TEXT,
	"collectionid"	INTEGER,
	"collectionname"	TEXT,
	"username"	TEXT,
	"userid"	INTEGER,
	"recorddatetime"	TEXT,
	"exported"	INTEGER,
	"exportdatetime"	TEXT,
	"exportuserid"	INTEGER,
	"agentfirstname"	TEXT,
	"agentmiddleinitial"	TEXT,
	"agentlastname"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("collectionid") REFERENCES "collection"("id"),
	FOREIGN KEY("institutionid") REFERENCES "institution"("id")
);
DROP TABLE IF EXISTS "storage";
CREATE TABLE "storage" (
	"id"	INTEGER NOT NULL UNIQUE,
	"spid"	INTEGER,
	"name"	TEXT,
	"fullname"	TEXT,
	"parentfullname"	TEXT,
	"collectionid"	INTEGER,
	"treedefid"	INTEGER,
	"rankname"	TEXT,
	"idnumber"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "taxonname";
CREATE TABLE "taxonname" (
	"id"	INTEGER NOT NULL UNIQUE,
	"spid"	INTEGER,
	"dwcid"	INTEGER,
	"dasscoid"	TEXT,
	"name"	TEXT,
	"author"	TEXT,
	"fullname"	TEXT,
	"rankid"	INTEGER,
	"taxonrank"	TEXT,
	"parentfullname"	TEXT,
	"acceptedfullname"	TEXT,
	"idnumber"	TEXT,
	"taxonnrsource"	TEXT,
	"treedefid"	INTEGER,
	"institutionid"	INTEGER,
	"collectionid"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "taxonname_fts";
CREATE VIRTUAL TABLE taxonname_fts USING fts5(id, name, fullname, rankid, taxontreedefid, institutionid);
DROP TABLE IF EXISTS "taxonname_fts_config";
CREATE TABLE 'taxonname_fts_config'(k PRIMARY KEY, v) WITHOUT ROWID;
DROP TABLE IF EXISTS "taxonname_fts_content";
CREATE TABLE 'taxonname_fts_content'(id INTEGER PRIMARY KEY, c0, c1, c2, c3, c4, c5);
DROP TABLE IF EXISTS "taxonname_fts_data";
CREATE TABLE 'taxonname_fts_data'(id INTEGER PRIMARY KEY, block BLOB);
DROP TABLE IF EXISTS "taxonname_fts_docsize";
CREATE TABLE 'taxonname_fts_docsize'(id INTEGER PRIMARY KEY, sz BLOB);
DROP TABLE IF EXISTS "taxonname_fts_idx";
CREATE TABLE 'taxonname_fts_idx'(segid, term, pgno, PRIMARY KEY(segid, term)) WITHOUT ROWID;
DROP TABLE IF EXISTS "taxonrank";
CREATE TABLE taxonrank (
	rankid INT,
	rankname VARCHAR(20)
);
DROP TABLE IF EXISTS "typestatus";
CREATE TABLE "typestatus" (
	"id"	INTEGER NOT NULL UNIQUE,
	"spid"	INTEGER,
	"name"	TEXT,
	"value"	TEXT,
	"ordinal"	INTEGER,
	"collectionid"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "user";
CREATE TABLE "user" (
	"id"	INTEGER NOT NULL UNIQUE,
	"spid"	INTEGER,
	"username"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "collection" ("id","spid","name","institutionid","taxontreedefid","visible","catalognrlength","usetaxonnumbers") VALUES (1,4,'NHMD Vertebrate Paleontology',1,1,0,9,NULL),
 (2,163841,'NHMD Entomology',1,5,1,9,NULL),
 (3,327682,'NHMD Invertebrate Paleontology',1,7,0,9,NULL),
 (4,425985,'NHMD Invertebrate Zoology',1,9,0,9,NULL),
 (5,458754,'NHMD Ornithology',1,10,0,9,NULL),
 (6,491522,'NHMD Mammalogy',1,11,0,9,NULL),
 (7,557056,'NHMD Quaternary Zoology',1,1,0,9,NULL),
 (8,589825,'NHMD Herpetology',1,12,0,9,NULL),
 (9,622592,'NHMD Archaeozoology Comparative Birds',1,10,0,9,NULL),
 (10,655360,'NHMD Archaeozoology Comparative Mammals',1,11,0,9,NULL),
 (11,688130,'NHMD Vascular Plants',1,13,1,8,NULL),
 (12,720897,'NHMD Biocultural Collection',1,14,0,9,NULL),
 (13,753665,'NHMD Danekrae',1,15,0,9,NULL),
 (14,786432,'NHMD Amber',1,5,0,9,NULL),
 (15,851970,'NHMD Ichthyology',1,17,0,9,NULL),
 (16,884736,'NHMD Mycology',1,13,0,9,NULL),
 (17,950274,'NHMD Exhibitions',1,18,0,9,NULL),
 (18,983040,'NHMD Micropaleontology',1,7,0,9,NULL),
 (19,32769,'NHMA Entomology',2,2,1,9,1),
 (20,3,'AU Herbarium',3,1,0,9,NULL),
 (21,950272,'NHMD Micropaleontology',1,7,0,9,NULL);
INSERT INTO "dummyrecord" ("id","spid","name","fullname") VALUES (0,0,'-error loading rows-','-error loading rows-');
INSERT INTO "institution" ("id","code","name","url","visible") VALUES (1,'NHMD','Natural History Museum of Denmark','https://specify-snm.science.ku.dk/',1),
 (2,'NHMA','Natural History Museum Aarhus','https://specify-nhma.science.ku.dk/',1),
 (3,'AU','Aarhus University Herbarium','https://specify-test.science.ku.dk/',0),
 (4,'MMG','Museum Mors & Fur Museum',' https://specify-muserum.science.ku.dk/',0),
 (5,'FIMUS','Fiskeri- og Søfartmuseet','https://specify-fimus.science.ku.dk/',0),
 (6,'MSJN','Museum Sønderjylland (Gram)','https://specify-msjn.science.ku.dk/',0),
 (7,'S','Naturama','https://specify-naturama.science.ku.dk/',0),
 (8,'OESM','Østsjællands Museum (Faxe)','https://specify-oesm.science.ku.dk/',0),
 (99,'TEST','Test Institution','https://specify-test.science.ku.dk/',0);
INSERT INTO "taxonname_fts_config" ("k","v") VALUES ('version',4);
INSERT INTO "taxonname_fts_data" ("id","block") VALUES (1,X''),
 (10,X'00000000000000');
INSERT INTO "taxonrank" ("rankid","rankname") VALUES (0,'Life'),
 (10,'Kingdom'),
 (20,'Subkingdom'),
 (30,'Phylum'),
 (30,'Division'),
 (40,'Subdivision'),
 (40,'Subphylum'),
 (50,'Superclass'),
 (60,'Class'),
 (70,'Subclass'),
 (80,'Infraclass'),
 (90,'Superorder'),
 (100,'Order'),
 (110,'Suborder'),
 (120,'Infraorder'),
 (130,'Superfamily'),
 (140,'Family'),
 (150,'Subfamily'),
 (160,'Tribe'),
 (170,'Subtribe'),
 (180,'Genus'),
 (190,'Subgenus'),
 (220,'Species'),
 (230,'Subspecies'),
 (240,'variety'),
 (250,'subvariety'),
 (260,'forma'),
 (270,'subforma');
DROP INDEX IF EXISTS "taxonfullname";
CREATE INDEX "taxonfullname" ON "taxonname" (
	"fullname"	ASC
);
COMMIT;
