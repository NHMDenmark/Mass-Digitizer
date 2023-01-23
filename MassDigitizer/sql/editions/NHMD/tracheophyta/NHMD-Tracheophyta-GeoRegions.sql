INSERT INTO "main"."georegion" ("name", "source", "collectionid") VALUES 
('Dania',  'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130)),
('Fennoscandia', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130)),
('Grønland', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130)),
('Europe', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130)),
('Africa', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130)),
('America centralis et australis et Antarctica', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130)),
('America septentrionalis', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130)),
('Asia', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130)),
('Australia et Oceania', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130)),
('Færøerne', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130)),
('Iceland', 'Major biogeographical region (NHMD)', (SELECT id FROM collection WHERE spid = 688130));