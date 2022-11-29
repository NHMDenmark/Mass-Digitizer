### Getting taxon Specify IDs for all names at all ranks. This is the inner SQL query!
### The outer query picks out the taxonomic full-name and the rank ID for that name.
#### This is meant for the Specify _MySQL_ database. The Specify taxonomy is one of the cornerstones of the Digitization App's taxonomic spine. 

```

SELECT t1.taxonfullname , t1.rankid FROM
(SELECT 
	tking.TaxonID kingdom,
	tdivis.TaxonTreeDefID AS taxonTree,
	tdivis.TaxonID Division, 
	tsubdiv.TaxonID subdivision,
	tsuperC.TaxonID superclass,
	tclass.TaxonID Class,
	tsubcl.TaxonID subClass,
	tsuperO.TaxonID superOrder,
	torder.TaxonID `Order`, 
	tsubor.TaxonID subOrder,
	tsuperF.TaxonID superfamily,
	tfamil.TaxonID Family,
	tsubfam.TaxonID subfamily, 
	tgenus.TaxonID Genus,
	tspeci.TaxonID Species,
	tsubsp.TaxonID Subspecies,
	tsubsp.Name SubspeciesName,
	tvarie.TaxonID Variety, 
	tvarie.Name VarietyName,
	tforma.TaxonID Forma, 
	tsubform.TaxonID subforma,	
	COALESCE(tforma.TaxonID, tvarie.TaxonID, tsubsp.TaxonID, tspeci.TaxonID, tgenus.TaxonID, tfamil.TaxonID, torder.TaxonID) lowest_taxonID,
			REPLACE(COALESCE(IF(tforma.FullName IS NOT NULL,CONCAT(tgenus.name, ' ', tspeci.Name, ' ', tsubsp.Name, ' ', ' f. ', tforma.Name),NULL), 
				IF(tvarie.FullName IS NOT NULL,CONCAT(tgenus.name, ' ', tspeci.Name, ' var. ', tvarie.Name),NULL),
				IF(tsubsp.FullName IS NOT NULL,CONCAT(tgenus.name, ' ', tspeci.Name, ' ', tsubsp.Name),NULL), 
					tspeci.FullName, tgenus.FullName, tfamil.FullName, torder.FullName, tclass.FullName, tdivis.FullName), '*', '') TaxonFullName,
			#COALESCE(defitem.RankID, tforma.rankID, tvarie.rankID, tsubsp.rankID, tspeci.rankID, tgenus.rankID, tfamil.rankID) rankID 
			 COALESCE(tforma.rankID, tvarie.rankID, tsubsp.rankID, tspeci.rankID, tgenus.rankID, tfamil.RankID) rankID
	FROM taxon tking 
		LEFT JOIN taxon tdivis ON tdivis.ParentID = tking.TaxonID AND tdivis.RankID = 30 
		LEFT JOIN taxon tsubdiv ON tsubdiv.ParentID = tdivis.TaxonID AND tsubdiv.RankID = 40
		LEFT JOIN taxon tsuperC ON tsuperC.ParentID = tsubdiv.TaxonID AND tsuperC.RankID = 50 AND tsuperC.IsAccepted = TRUE
		LEFT JOIN taxon tclass ON tclass.ParentID = tdivis.TaxonID AND tclass.RankID = 60	AND tclass.IsAccepted = TRUE 
		LEFT JOIN taxon tsubcl ON tsubcl.ParentID = tclass.TaxonID AND tsubcl.RankID = 70	AND tsubcl.IsAccepted = TRUE 
		LEFT JOIN taxon tsuperO ON tsuperO.ParentID = tsubcl.TaxonID AND tsuperO.RankID = 90 AND tsuperO.IsAccepted = TRUE
		LEFT JOIN taxon torder ON torder.ParentID = tclass.TaxonID AND torder.RankID = 100 AND torder.IsAccepted = TRUE
		LEFT JOIN taxon tsubor ON tsubor.ParentID = torder.TaxonID AND tsubor.RankID = 110 AND tsubor.IsAccepted = TRUE	
		LEFT JOIN taxon tsuperF ON tsuperF.ParentID = tsubor.TaxonID AND tsuperF.RankID = 130 AND tsuperF.IsAccepted = TRUE
		LEFT JOIN taxon tfamil ON tfamil.ParentID = torder.TaxonID AND tfamil.RankID = 140 AND tfamil.IsAccepted = TRUE
		LEFT JOIN taxon tsubfam ON tsubfam.ParentID = tfamil.TaxonID AND tsubfam.RankID = 150 AND tsubfam.IsAccepted = TRUE
		LEFT JOIN taxon tgenus ON tgenus.ParentID = tfamil.TaxonID AND tgenus.RankID = 180 AND tgenus.IsAccepted = TRUE 
		LEFT JOIN taxon tspeci ON tspeci.ParentID = tgenus.TaxonID AND tspeci.RankID = 220 AND tspeci.IsAccepted = TRUE
		LEFT JOIN taxon tsubsp ON tsubsp.ParentID = tspeci.TaxonID AND tsubsp.RankID = 230 AND tsubsp.IsAccepted = TRUE 
		LEFT JOIN taxon tvarie ON tvarie.ParentID = tspeci.TaxonID AND tvarie.RankID = 240 AND tvarie.IsAccepted = TRUE 
		LEFT JOIN taxon tforma ON tforma.ParentID = tspeci.TaxonID AND tforma.RankID = 260 AND tforma.IsAccepted = TRUE
		LEFT JOIN taxon tsubform ON tsubform.ParentID = tforma.TaxonID AND tsubform.RankID = 270 AND tsubform.IsAccepted = TRUE
		LEFT JOIN taxontreedefitem defitem ON tdivis.TaxonTreeDefItemID = defitem.TaxonTreeDefItemID
	WHERE  tdivis.TaxonTreeDefID = 13 -- Discipline: Botany 
	GROUP BY TaxonFullName)t1 ORDER BY rankid; 

```
The field TaxonTreeDefID is set to 13 which is the discipline "Botany".
