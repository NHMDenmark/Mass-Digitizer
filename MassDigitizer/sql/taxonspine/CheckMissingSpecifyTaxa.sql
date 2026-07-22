SELECT COUNT(*)
FROM specify_taxon_staging s
LEFT JOIN taxa t
    ON t.sp_taxonID = s.sp_taxonID
WHERE t.id IS NULL;