-- SQL Script for extracting storage locations from Specify db for insertion into local app db
--
-- To be run on Specify database for each collection 
-- The generated lines should be added below the statement:
--     INSERT INTO storage (name, fullname, rankname, collectionid) VALUES 

SELECT CONCAT('("', t1.unit, '",', CONCAT( t1.stor), ' | ', t1.unit, '", ', '"',t1.rank_name, '", ', '(SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),') AS storage_  FROM
(
SELECT CONCAT_WS(' | ', '"Natural History Museum of Denmark' , t1.Name , t2.name ) AS stor, stdi.name AS rank_name,
  CASE 
    WHEN t2.storageid = 81648 THEN CONCAT('Box ', t3.Name)
    WHEN t2.storageid = 89805 THEN CONCAT('Shelf ', t3.Name)
	 ELSE t3.Name
  END AS unit,
  stdi.Name AS rankname, t3.name AS index_
FROM storage AS t1
LEFT JOIN storage AS t2 ON t2.ParentID = t1.storageID
LEFT JOIN storage AS t3 ON t3.parentID = t2.storageID
LEFT JOIN storagetreedefitem stdi ON t3.RankID = stdi.RankID
WHERE t2.storageid IN ( 81648, 89805) )t1;
-- The query is only three levels deep which makes it managable with LEFT JOINs. 
-- After running the query remember to remove the very last comma in the file.

