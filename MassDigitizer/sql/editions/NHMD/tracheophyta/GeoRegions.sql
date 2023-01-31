<<<<<<< HEAD
INSERT INTO "main"."georegion" ("name", "source", "collectionid") VALUES 
('Denmark',  'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
=======
INSERT INTO georegion ("name", "source", "collectionid") VALUES 
('None', 'none', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('Dania',  'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
>>>>>>> 7fd7b6f202ee18409348dfe0022c2c823f6e0926
('Fennoscandia', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('Grønland', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('Europe', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('Africa', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('America centralis et australis et Antarctica', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('America septentrionalis', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('Asia', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('Australia et Oceania', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('Færøerne', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
<<<<<<< HEAD
('Iceland', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('None', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),;
=======
('Island', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1))
;
>>>>>>> 7fd7b6f202ee18409348dfe0022c2c823f6e0926
