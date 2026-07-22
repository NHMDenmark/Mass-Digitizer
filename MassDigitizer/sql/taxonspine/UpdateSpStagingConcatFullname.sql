UPDATE specify_taxon_staging
SET sp_fullname = CONCAT(sp_fullname, ' ', sp_author)
WHERE sp_author IS NOT NULL
  AND sp_author <> ''
  AND sp_fullname NOT LIKE CONCAT('%', sp_author, '%');