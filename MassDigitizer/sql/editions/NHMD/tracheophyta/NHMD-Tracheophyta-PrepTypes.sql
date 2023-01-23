INSERT INTO preptype ("spid","name","collectionid") VALUES 
 (134,"Dried", (SELECT id FROM collection WHERE spid = 688130))
,(135,"Boxed", (SELECT id FROM collection WHERE spid = 688130))
,(136,"Fluid", (SELECT id FROM collection WHERE spid = 688130))
,(137,"Sheet", (SELECT id FROM collection WHERE spid = 688130));

