  -- To be run on Specify database for each collection 
SELECT CONCAT_WS(' | ', s1.institution, s1.building, s1.collection, s1.unit) FROM
  (SELECT 'Natural History Museum of Denmark' AS institution, t1.Name AS building, t2.name AS collection, 
    case when t2.Name = 'Herbarium C: Danish Vascular Plant Collection' then CONCAT('Box ', t3.Name)
    ELSE CONCAT('Shelf ', t3.Name)
    END AS unit
  FROM storage AS t1
  LEFT JOIN storage AS t2 ON t2.ParentID = t1.storageID
  LEFT JOIN storage AS t3 ON t3.parentID = t2.storageID
  WHERE t1.Name IN ( 'Priorparken') AND t2.Name LIKE ('Herbarium%'))s1;

-- The query is only three levels deep which makes it managable with LEFT JOINs. An alternative would be to use CTE (Common Table Expressions).


 		 
