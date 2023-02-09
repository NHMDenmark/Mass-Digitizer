INSERT INTO "main"."georegion" ("name", "source", "collectionid") VALUES 
('Dania',  'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('None', 'none', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('Fennoscandia', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('Grønland', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('Europe', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('Africa', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('America centralis et australis et Antarctica', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('America septentrionalis', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('Asia', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('Australia et Oceania', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('Færøerne', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),
('Island', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1));


