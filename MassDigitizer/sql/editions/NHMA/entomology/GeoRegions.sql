INSERT INTO "main"."georegion" ("name", "source", "collectionid") VALUES 
 ('Denmark', '', (SELECT id FROM collection WHERE spid = 32769 AND institutionid = 2))
;
