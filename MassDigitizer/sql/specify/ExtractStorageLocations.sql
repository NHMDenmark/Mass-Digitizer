SELECT DISTINCT storage_ FROM (
SELECT CONCAT('("', t1.unit, '",', CONCAT(t1.stor), ' | ', t1.unit, '", ', '"', t1.rank_name, '", ', '(SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),') AS storage_
	 	 ,t1.sort_unit, t1.sort_coll -- Include sorting in the final output
FROM (
    SELECT CONCAT_WS(' | ', '"Natural History Museum of Denmark', st1.Name) AS stor,
           stdi.name AS rank_name,
           st2.Name AS unit,
           stdi.Name AS rankname,
           st2.name AS index_,
           st2.name AS sort_coll,
           CAST(REGEXP_REPLACE(st2.Name, '[^0-9]', '') AS UNSIGNED) AS sort_unit
    FROM storage AS st1
    LEFT JOIN storage AS st2 ON st2.ParentID = st1.storageID
    LEFT JOIN storagetreedefitem stdi ON st2.RankID = stdi.RankID
    WHERE st2.storageid IN (81648, 89805) 

    UNION ALL
    
    SELECT CONCAT_WS(' | ', '"Natural History Museum of Denmark', st1.Name, st2.name) AS stor,
           stdi.name AS rank_name,
           CASE 
               WHEN st2.storageid = 81648 THEN CONCAT('Box ', st3.Name)
               WHEN st2.storageid = 89805 THEN CONCAT('Shelf ', st3.Name)
               ELSE st3.Name
           END AS unit,
           stdi.Name AS rankname,
           st3.name AS index_,
           st2.name AS sort_coll,
           CAST(REGEXP_REPLACE(st3.Name, '[^0-9]', '') AS UNSIGNED) AS sort_unit
    FROM storage AS st1
    LEFT JOIN storage AS st2 ON st2.ParentID = st1.storageID
    LEFT JOIN storage AS st3 ON st3.parentID = st2.storageID
    LEFT JOIN storagetreedefitem stdi ON st3.RankID = stdi.RankID
    WHERE st2.storageid IN (81648, 89805)
) t1

UNION ALL

SELECT CONCAT('("', t2.unit, '",', CONCAT(t2.stor), ' | ', t2.unit, '", ', '"', t2.rank_name, '", ', '(SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1)),') AS storage_
		 ,t2.sort_unit, t2.sort_coll -- Include sorting in the final output
FROM (
    SELECT CONCAT_WS(' | ', '"Natural History Museum of Denmark', st1.Name) AS stor,
           stdi.name AS rank_name,
           st2.Name AS unit,
           stdi.Name AS rankname,
           st2.name AS index_,
           st2.name AS sort_coll,
           CAST(REGEXP_REPLACE(st2.Name, '[^0-9]', '') AS UNSIGNED) AS sort_unit
    FROM storage AS st1
    LEFT JOIN storage AS st2 ON st2.ParentID = st1.storageID
    LEFT JOIN storagetreedefitem stdi ON st2.RankID = stdi.RankID
    WHERE st2.storageid IN (372531) 

    UNION ALL
    
    SELECT CONCAT_WS(' | ', '"Natural History Museum of Denmark', st1.Name, st2.name) AS stor,
           stdi.name AS rank_name,
           CONCAT('Cabinet ', st3.Name) AS unit,
           stdi.Name AS rankname,
           st3.name AS index_,
           st2.name AS sort_coll,
           CAST(REGEXP_REPLACE(st3.Name, '[^0-9]', '') AS UNSIGNED) AS sort_unit
    FROM storage AS st1
    LEFT JOIN storage AS st2 ON st2.ParentID = st1.storageID
    LEFT JOIN storage AS st3 ON st3.parentID = st2.storageID
    LEFT JOIN storagetreedefitem stdi ON st3.RankID = stdi.RankID
    WHERE st2.storageid IN (372531) 

    UNION ALL

    SELECT CONCAT_WS(' | ', '"Natural History Museum of Denmark', st1.Name, st2.name, CONCAT('Cabinet ', st3.name)) AS stor,
           stdi.name AS rank_name,
           CONCAT('Shelf ', st4.Name) AS unit,
           stdi.Name AS rankname,
           st4.name AS index_,
           st2.name AS sort_coll,
           CAST(REGEXP_REPLACE(st3.Name, '[^0-9]', '') AS UNSIGNED) AS sort_unit
    FROM storage AS st1
    LEFT JOIN storage AS st2 ON st2.ParentID = st1.storageID
    LEFT JOIN storage AS st3 ON st3.parentID = st2.storageID
    LEFT JOIN storage AS st4 ON st4.parentID = st3.storageID
    LEFT JOIN storagetreedefitem stdi ON st4.RankID = stdi.RankID
    WHERE st2.storageid IN (372531) 
    
) t2

ORDER BY sort_coll, sort_unit
) t_all
;
-- 39.288