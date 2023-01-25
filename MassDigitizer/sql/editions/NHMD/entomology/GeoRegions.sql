INSERT INTO "main"."georegion" ("name", "source", "collectionid") VALUES 
 ('Nearctic',     'Major biogeographical region (Hansen 1998, World Catalogue of Insects)', (SELECT id FROM collection WHERE spid = 163841 AND institutionid = 1))
,('Neotropical',  'Major biogeographical region (Hansen 1998, World Catalogue of Insects)', (SELECT id FROM collection WHERE spid = 163841 AND institutionid = 1))
,('Palearctic',   'Major biogeographical region (Hansen 1998, World Catalogue of Insects)', (SELECT id FROM collection WHERE spid = 163841 AND institutionid = 1))
,('Afrotropical', 'Major biogeographical region (Hansen 1998, World Catalogue of Insects)', (SELECT id FROM collection WHERE spid = 163841 AND institutionid = 1))
,('Oriental',     'Major biogeographical region (Hansen 1998, World Catalogue of Insects)', (SELECT id FROM collection WHERE spid = 163841 AND institutionid = 1))
,('Australian',   'Major biogeographical region (Hansen 1998, World Catalogue of Insects)', (SELECT id FROM collection WHERE spid = 163841 AND institutionid = 1))
