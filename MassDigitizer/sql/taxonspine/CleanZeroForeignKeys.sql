
UPDATE taxa
SET dwc_parentNameUsageID = NULL
WHERE dwc_parentNameUsageID = 0;

UPDATE taxa
SET dwc_acceptedNameUsageID = NULL
WHERE dwc_acceptedNameUsageID = 0;

UPDATE taxa
SET sp_taxonID = NULL
WHERE sp_taxonID = 0;

UPDATE taxa t SET t.sp_taxontreedefid = 13;