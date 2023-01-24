INSERT INTO preptype ("spid","name","collectionid") VALUES 
 (0,"Pinned", (SELECT id FROM collection WHERE spid = 163841 AND institutionid = 1))
 ;

