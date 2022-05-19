SELECT 				
        tdivis.TaxonTreeDefID AS taxonTree,
        --tdivis.TaxonID Division, 
        tdivis.name,
        tclass.TaxonID Class,
        tclass.name,
        torder.TaxonID `Order`, 
        torder.name,
        tfamil.TaxonID Family,
		  tfamil.name, 
        tgenus.TaxonID Genus,
        tgenus.name,
        -- tgenus.Name Genusname,
        tspeci.TaxonID Species,
		  tspeci.name, 
        -- tspeci.Name Speciesname,
        tsubsp.TaxonID Subspecies,
		  tsubsp.name ,
        -- tsubsp.Name SubspeciesName,
        tvarie.TaxonID Variety, 
         tvarie.Name VarietyName,
        tforma.TaxonID Forma, 
        -- tforma.Name FormaName,
        COALESCE(tforma.TaxonID, tvarie.TaxonID, tsubsp.TaxonID, tspeci.TaxonID, tgenus.TaxonID, tfamil.TaxonID, torder.TaxonID) lowest_taxonID,
		  REPLACE(COALESCE(IF(tforma.FullName IS NOT NULL,CONCAT(tgenus.name, ' ', tspeci.Name, ' ', tsubsp.Name, ' ', ' f. ', tforma.Name),NULL), 
		           IF(tvarie.FullName IS NOT NULL,CONCAT(tgenus.name, ' ', tspeci.Name, ' var. ', tvarie.Name),NULL),
					  IF(tsubsp.FullName IS NOT NULL,CONCAT(tgenus.name, ' ', tspeci.Name, ' ', tsubsp.Name),NULL), 
					  tspeci.FullName, tgenus.FullName, tfamil.FullName, torder.FullName, tclass.FullName, tdivis.FullName), '*', '') TaxonFullName,
			#COALESCE(defitem.RankID, tforma.rankID, tvarie.rankID, tsubsp.rankID, tspeci.rankID, tgenus.rankID, tfamil.rankID) rankID 
			 COALESCE(tforma.rankID, tvarie.rankID, tsubsp.rankID, tspeci.rankID, tgenus.rankID, tfamil.RankID) rankID
    FROM taxon tdivis 
        LEFT JOIN taxon tclass ON tclass.ParentID = tdivis.TaxonID AND tclass.RankID = 60  AND tclass.IsAccepted = TRUE 
        LEFT JOIN taxon torder ON torder.ParentID = tclass.TaxonID AND torder.RankID = 100 AND torder.IsAccepted = TRUE  
        LEFT JOIN taxon tfamil ON tfamil.ParentID = torder.TaxonID AND tfamil.RankID = 140 AND tfamil.IsAccepted = TRUE 
        LEFT JOIN taxon tgenus ON tgenus.ParentID = tfamil.TaxonID AND tgenus.RankID = 180 AND tgenus.IsAccepted = TRUE 
        LEFT JOIN taxon tspeci ON tspeci.ParentID = tgenus.TaxonID AND tspeci.RankID = 220 AND tspeci.IsAccepted = TRUE 
        LEFT JOIN taxon tsubsp ON tsubsp.ParentID = tspeci.TaxonID AND tsubsp.RankID = 230 AND tsubsp.IsAccepted = TRUE 
        LEFT JOIN taxon tvarie ON tvarie.ParentID = tspeci.TaxonID AND tvarie.RankID = 240 AND tvarie.IsAccepted = TRUE 
        LEFT JOIN taxon tforma ON tforma.ParentID = tspeci.TaxonID AND tforma.RankID = 260 AND tforma.IsAccepted = TRUE
		  LEFT JOIN taxontreedefitem defitem ON tdivis.TaxonTreeDefItemID = defitem.TaxonTreeDefItemID
		  
    WHERE tdivis.ParentID = 317960 -- Plantae kingdom  
      AND tdivis.TaxonTreeDefID = 13
		GROUP BY TaxonFullName ; -- Tree belonging to discipline: Botany
