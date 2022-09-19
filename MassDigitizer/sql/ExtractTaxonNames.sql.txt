 SELECT 	
	-- t.TaxonID taxonid, -- t.Name name, t.FullName fullname, t.RankID rankid, t.TaxonTreeDefID taxontreedefid, p1.FullName parentfullname, 
	CONCAT('INSERT INTO taxonname ("taxonid","name","fullname","rankid","taxontreedefid","parentfullname") VALUES (',
			 t.TaxonID, ',"', t.Name, '","', t.FullName, '",', t.RankID, ',', t.TaxonTreeDefID, ',"', p1.FullName,'");') 
	sqlstatement 
 FROM taxon t 
	JOIN taxon p1 ON p1.TaxonID = t.ParentID
	WHERE 
		t.taxontreedefid = 13
		AND t.FullName NOT LIKE '%*%' 
		AND t.fullname NOT LIKE '%.%' 
LIMIT 300000 -- OFFSET 300000