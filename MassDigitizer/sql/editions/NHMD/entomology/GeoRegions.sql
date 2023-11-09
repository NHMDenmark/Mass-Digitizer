INSERT INTO georegion ("name", "source", "collectionid") VALUES 
('None',         'none', (SELECT id FROM collection WHERE spid = 163841 AND institutionid = 1)),
('Nearctic',     'Major biogeographical region (Hansen 1998, World Catalogue of Insects)', (SELECT id FROM collection WHERE spid = 163841 AND institutionid = 1)),
('Neotropical',  'Major biogeographical region (Hansen 1998, World Catalogue of Insects)', (SELECT id FROM collection WHERE spid = 163841 AND institutionid = 1)),
('Palearctic',   'Major biogeographical region (Hansen 1998, World Catalogue of Insects)', (SELECT id FROM collection WHERE spid = 163841 AND institutionid = 1)),
('Afrotropical', 'Major biogeographical region (Hansen 1998, World Catalogue of Insects)', (SELECT id FROM collection WHERE spid = 163841 AND institutionid = 1)),
('Oriental',     'Major biogeographical region (Hansen 1998, World Catalogue of Insects)', (SELECT id FROM collection WHERE spid = 163841 AND institutionid = 1)),
('Australian',   'Major biogeographical region (Hansen 1998, World Catalogue of Insects)', (SELECT id FROM collection WHERE spid = 163841 AND institutionid = 1)),
('Dania',      '', (SELECT id FROM collection WHERE spid = 163841 AND institutionid = 1))
;