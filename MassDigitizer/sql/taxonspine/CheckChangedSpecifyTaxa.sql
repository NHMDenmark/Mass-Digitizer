SELECT
    t.dassco_fullname, t.dwc_scientificName, 
    t.sp_fullname, s.sp_fullname,
    t.sp_author, s.sp_author,
    t.sp_rankid, LPAD(s.sp_rankid,3,'0'),
    t.sp_rankname, s.sp_rankname,
    t.sp_parentname, s.sp_parentname,
    t.sp_taxonnr, s.sp_taxonnr,
    t.sp_taxontreedefid, s.sp_taxontreedefid
FROM taxa t
JOIN specify_taxon_staging s ON t.sp_taxonID = s.sp_taxonID
WHERE
       COALESCE(t.sp_fullname,'') <> COALESCE(s.sp_fullname,'')
    OR COALESCE(t.sp_author,'') <> COALESCE(s.sp_author,'')
    OR LPAD(COALESCE(t.sp_rankid,''),3,'0')
       <> LPAD(COALESCE(s.sp_rankid,''),3,'0')
    OR COALESCE(t.sp_rankname,'') <> COALESCE(s.sp_rankname,'')
    OR COALESCE(t.sp_parentname,'') <> COALESCE(s.sp_parentname,'')
    OR COALESCE(t.sp_taxonnr,'') <> COALESCE(s.sp_taxonnr,'')
    OR COALESCE(t.sp_taxontreedefid,0)
       <> COALESCE(s.sp_taxontreedefid,0)
	 ORDER BY t.sp_fullname;