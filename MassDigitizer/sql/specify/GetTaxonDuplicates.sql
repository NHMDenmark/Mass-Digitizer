SELECT DISTINCT(t1.TaxonID) -- , t2.TaxonID, t1.FullName, t1.Author, t2.FullName, t2.Author  
FROM taxon t1 
	LEFT JOIN taxon t2 ON t1.FullName = t2.FullName AND t1.TaxonID <> t2.TaxonID 
	WHERE t1.TaxonTreeDefID = 17 
	  AND t2.TaxonTreeDefID = 17
	  AND t1.RankID >= 180 AND t2.RankID >= 180 -- Restrict to genus and below 
	  
	  ORDER BY t1.TaxonId ;