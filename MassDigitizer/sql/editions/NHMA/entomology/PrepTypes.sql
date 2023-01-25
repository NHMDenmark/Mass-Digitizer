INSERT INTO preptype ("spid","name","collectionid") VALUES 
 (0,"Pinned", (SELECT id FROM collection WHERE spid = 32769 AND institutionid = 2))
 ;

