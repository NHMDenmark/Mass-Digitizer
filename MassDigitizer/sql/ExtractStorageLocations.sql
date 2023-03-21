  -- To be run on Specify database for each collection 
SELECT CONCAT_WS(' | ', CONCAT('(', t1.stor), t1.unit, t1.rank_name, '(SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),') AS storage_  FROM
(
SELECT CONCAT_WS(' | ', 'Natural History Museum of Denmark' , t1.Name , t2.name ) AS stor, stdi.name AS rank_name,
case when t2.Name = 'Herbarium C: Danish Vascular Plant Collection' then CONCAT('Box ', t3.Name)
ELSE CONCAT('Shelf ', t3.Name)
END AS unit, stdi.Name AS rankname, t3.name AS index_
FROM storage AS t1
LEFT JOIN storage AS t2 ON t2.ParentID = t1.storageID
LEFT JOIN storage AS t3 ON t3.parentID = t2.storageID
LEFT JOIN storagetreedefitem stdi ON t3.RankID = stdi.RankID
WHERE t1.Name IN ( 'Priorparken') AND t2.Name LIKE ('Herbarium%')
)t1;