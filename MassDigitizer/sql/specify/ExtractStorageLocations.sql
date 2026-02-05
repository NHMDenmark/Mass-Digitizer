
WITH t1 AS (
  /* Room (RankID 200 at st2) */
  SELECT 
    CONCAT_WS(' | ', st1.Name, st2.Name) AS stor,
    stdi.Name AS rank_name,
    stdi.RankID AS rank_id,
    st2.Name AS unit,
    st2.StorageID,
    stdi.Name AS rankname,
    st2.Name AS index_,
    st2.Name AS sort_coll,
    CAST(REGEXP_REPLACE(st2.Name, '[^0-9]', '') AS UNSIGNED) AS sort_unit
  FROM storage AS st1
  LEFT JOIN storage AS st2 ON st2.ParentID = st1.StorageID
  LEFT JOIN storagetreedefitem stdi ON st2.RankID = stdi.RankID
  WHERE st2.StorageID IN (81648, 89805, 372531, 1433)
    AND stdi.RankID = 200

  UNION ALL

  /* Aisle (RankID 250 at st3) */
  SELECT 
    CONCAT_WS(' | ', st1.Name, st2.Name, st3.Name) AS stor,
    stdi.Name AS rank_name,
    stdi.RankID AS rank_id,
    st3.Name AS unit,
    st3.StorageID,
    stdi.Name AS rankname,
    st3.Name AS index_,
    st2.Name AS sort_coll,
    CAST(REGEXP_REPLACE(st3.Name, '[^0-9]', '') AS UNSIGNED) AS sort_unit
  FROM storage AS st1
  LEFT JOIN storage AS st2 ON st2.ParentID = st1.StorageID
  LEFT JOIN storage AS st3 ON st3.ParentID = st2.StorageID
  LEFT JOIN storagetreedefitem stdi ON st3.RankID = stdi.RankID
  WHERE st2.StorageID IN (81648, 89805, 372531, 1433)
    AND stdi.RankID = 250

  UNION ALL

  /* Cabinet (RankID 300 at st4) */
  SELECT 
    CONCAT_WS(' | ', st1.Name, st2.Name, st3.Name, CONCAT('Cabinet ', st4.Name)) AS stor, 
    stdi.Name AS rank_name,
    stdi.RankID AS rank_id,
    CONCAT('Cabinet ', st4.Name) AS unit,         
    st4.StorageID,
    stdi.Name AS rankname,
    st4.Name AS index_,
    st2.Name AS sort_coll,
    CAST(REGEXP_REPLACE(st4.Name, '[^0-9]', '') AS UNSIGNED) AS sort_unit
  FROM storage AS st1
  LEFT JOIN storage AS st2 ON st2.ParentID = st1.StorageID
  LEFT JOIN storage AS st3 ON st3.ParentID = st2.StorageID
  LEFT JOIN storage AS st4 ON st4.ParentID = st3.StorageID
  LEFT JOIN storagetreedefitem AS stdi ON st4.RankID = stdi.RankID
  WHERE st2.StorageID IN (81648, 89805, 372531, 1433)
    AND stdi.RankID = 300

  UNION ALL

  /* Shelf under Aisle (RankID 350 at st4) */
  SELECT DISTINCT 
    CONCAT_WS(' | ', st1.Name, st2.Name, st3.Name, CONCAT('Shelf ', st4.Name)) AS stor, 
    stdi.Name AS rank_name,
    stdi.RankID AS rank_id,
    CONCAT('Shelf ', st4.Name) AS unit,
    st4.StorageID,
    stdi.Name AS rankname,
    st4.Name AS index_,
    st2.Name AS sort_coll,
    CAST(REGEXP_REPLACE(st4.Name, '[^0-9]', '') AS UNSIGNED) AS sort_unit
  FROM storage AS st1
  LEFT JOIN storage AS st2 ON st2.ParentID = st1.StorageID
  LEFT JOIN storage AS st3 ON st3.ParentID = st2.StorageID
  LEFT JOIN storage AS st4 ON st4.ParentID = st3.StorageID
  LEFT JOIN storagetreedefitem AS stdi ON st4.RankID = stdi.RankID
  WHERE st2.StorageID IN (81648, 89805, 372531, 1433)
    AND stdi.RankID = 350

  UNION ALL

  /* Shelf under Cabinet (RankID 350 at st5) */
  SELECT 
    CONCAT_WS(' | ', st1.Name, st2.Name, st3.Name, CONCAT('Cabinet ', st4.Name), CONCAT('Shelf ', st5.Name)) AS stor, 
    stdi.Name AS rank_name,
    stdi.RankID AS rank_id,
    CONCAT('Shelf ', st5.Name) AS unit,
    st5.StorageID,
    stdi.Name AS rankname,
    st5.Name AS index_,
    st2.Name AS sort_coll,
    CAST(REGEXP_REPLACE(st5.Name, '[^0-9]', '') AS UNSIGNED) AS sort_unit
  FROM storage AS st1
  LEFT JOIN storage AS st2 ON st2.ParentID = st1.StorageID
  LEFT JOIN storage AS st3 ON st3.ParentID = st2.StorageID
  LEFT JOIN storage AS st4 ON st4.ParentID = st3.StorageID
  LEFT JOIN storage AS st5 ON st5.ParentID = st4.StorageID
  LEFT JOIN storagetreedefitem AS stdi ON st5.RankID = stdi.RankID
  WHERE st2.StorageID IN (81648, 89805, 372531, 1433)
    AND stdi.RankID = 350

  UNION ALL

  /* Rack under Shelf (RankID 450 at st5) */
  SELECT 
    CONCAT_WS(' | ', st1.Name, st2.Name, st3.Name, CONCAT('Shelf ', st4.Name), CONCAT('Rack ', st5.Name)) AS stor, 
    stdi.Name AS rank_name,
    stdi.RankID AS rank_id,
    CONCAT('Rack ', st5.Name) AS unit,
    st5.StorageID,
    stdi.Name AS rankname,
    st5.Name AS index_,
    st2.Name AS sort_coll,
    CAST(REGEXP_REPLACE(st5.Name, '[^0-9]', '') AS UNSIGNED) AS sort_unit
  FROM storage AS st1
  LEFT JOIN storage AS st2 ON st2.ParentID = st1.StorageID
  LEFT JOIN storage AS st3 ON st3.ParentID = st2.StorageID
  LEFT JOIN storage AS st4 ON st4.ParentID = st3.StorageID
  LEFT JOIN storage AS st5 ON st5.ParentID = st4.StorageID
  LEFT JOIN storagetreedefitem AS stdi ON st5.RankID = stdi.RankID
  WHERE st2.StorageID IN (81648, 89805, 372531, 1433)
    AND stdi.RankID = 450

  UNION ALL

  /* Rack under Aisle (RankID 450 at st4) */
  SELECT 
    CONCAT_WS(' | ', st1.Name, st2.Name, st3.Name, CONCAT('Rack ', st4.Name)) AS stor, 
    stdi.Name AS rank_name,
    stdi.RankID AS rank_id,
    CONCAT('Rack ', st4.Name) AS unit,
    st4.StorageID,
    stdi.Name AS rankname,
    st4.Name AS index_,
    st2.Name AS sort_coll,
    CAST(REGEXP_REPLACE(st4.Name, '[^0-9]', '') AS UNSIGNED) AS sort_unit
  FROM storage AS st1
  LEFT JOIN storage AS st2 ON st2.ParentID = st1.StorageID
  LEFT JOIN storage AS st3 ON st3.ParentID = st2.StorageID
  LEFT JOIN storage AS st4 ON st4.ParentID = st3.StorageID
  LEFT JOIN storagetreedefitem AS stdi ON st4.RankID = stdi.RankID
  WHERE st2.StorageID IN (81648, 89805, 372531, 1433)
    AND stdi.RankID = 450
    
    
	UNION ALL
	
	/* Box under Aisle (RankID 400 at st4) */
	SELECT 
	  CONCAT_WS(' | ',
	    st1.Name,
	    st2.Name,
	    st3.Name,
	    CONCAT('Box ', st4.Name)
	  ) AS stor,
	  stdi.Name AS rank_name,
	  stdi.RankID AS rank_id,
	  CONCAT('Box ', st4.Name) AS unit,
	  st4.StorageID,
	  stdi.Name AS rankname,
	  st4.Name AS index_,
	  st2.Name AS sort_coll,
	  CAST(REGEXP_REPLACE(st4.Name, '[^0-9]', '') AS UNSIGNED) AS sort_unit
	FROM storage AS st1
	LEFT JOIN storage AS st2 ON st2.ParentID = st1.StorageID       -- Room
	LEFT JOIN storage AS st3 ON st3.ParentID = st2.StorageID       -- Aisle
	LEFT JOIN storage AS st4 ON st4.ParentID = st3.StorageID       -- Box
	LEFT JOIN storagetreedefitem AS stdi ON st4.RankID = stdi.RankID
	WHERE st2.StorageID IN (81648, 89805, 372531, 1433)
	  AND stdi.RankID = 400  -- Box
),
prepared AS (
  SELECT
    CONCAT(
      '("', unit, '", ',
      '"', stor, '", ',
      '"', rank_name, '", ',
      '(SELECT id FROM collection WHERE spid = 688130 AND institutionid = 1))'
    ) AS storage_,
    sort_coll,
    sort_unit,
    rank_id
  FROM t1
),
dedup AS (
  SELECT
    storage_,
    sort_coll,
    sort_unit,
    rank_id,
    ROW_NUMBER() OVER (
      PARTITION BY storage_
      ORDER BY rank_id, sort_coll, sort_unit
    ) AS rn
  FROM prepared
)
SELECT storage_
FROM dedup
WHERE rn = 1
ORDER BY rank_id, sort_coll, sort_unit;
