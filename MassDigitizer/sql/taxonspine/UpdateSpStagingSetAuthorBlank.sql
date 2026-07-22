UPDATE specify_taxon_staging s SET s.sp_author = '' WHERE s.sp_author IS NULL;
UPDATE specify_taxon_staging s SET s.sp_taxonnr = '' WHERE s.sp_taxonnr IS NULL;