  -- To be run on Specify database 
  SELECT 	
	-- t.TaxonID taxonid, -- t.Name name, t.FullName fullname, t.RankID rankid, t.TaxonTreeDefID taxontreedefid, p1.FullName parentfullname, 
	CONCAT(
	-- 'INSERT INTO taxonname ("spid","name","fullname","rankid","taxontreedefid","parentfullname", "collectionid") VALUES (', 
	',(', t.TaxonID, ',"', t.Name, '","', t.FullName, '",', t.RankID, ',', t.TaxonTreeDefID, ',"', p1.FullName,'", (SELECT id FROM collection WHERE spid = ', pt.CollectionID, '))') 
	sqlstatement 
 FROM taxon t 
	JOIN taxon p1 ON p1.TaxonID = t.ParentID
	WHERE 
		t.taxontreedefid = 13
		AND t.FullName NOT LIKE '%*%' 
		AND t.fullname NOT LIKE '%.%' 
		AND t.RankID <= 180 -- Highertaxa (including Genus)
		-- AND t.RankID = 240 -- Species 
		-- AND t.RankID = 230 -- Subspecies 
	ORDER BY t.RankID -- For higher taxa
	-- ORDER BY t.fullName -- For species and below
LIMIT 250000 -- OFFSET 250000