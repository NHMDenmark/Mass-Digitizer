INSERT INTO georegion ("name", "source", "collectionid") VALUES 
('None',         'none', (SELECT id FROM collection WHERE spid = 327682 AND institutionid = 1)),
('Denmark',      '', (SELECT id FROM collection WHERE spid = 327682 AND institutionid = 1))
;