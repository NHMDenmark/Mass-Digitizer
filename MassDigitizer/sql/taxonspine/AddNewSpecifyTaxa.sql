/* Add new Specify taxa */

INSERT INTO taxa (
    dassco_taxonID,
    dassco_name,
    dassco_author,
    dassco_fullname,
    dassco_rankid,

    sp_taxonID,
    sp_fullname,
    sp_author,
    sp_rankid,
    sp_rankname,
    sp_parentname,
    sp_taxonnr,
    sp_taxonnrsource,
    sp_taxontreedefid,
    sp_institutionID
)
SELECT
    MD5(UUID()),

    s.sp_fullname,
    s.sp_author,
    s.sp_fullname,
    LPAD(s.sp_rankid, 3, '0'),

    s.sp_taxonID,
    s.sp_fullname,
    s.sp_author,
    LPAD(s.sp_rankid, 3, '0'),
    s.sp_rankname,
    s.sp_parentname,
    s.sp_taxonnr,
    'Specify',
    s.sp_taxontreedefid,
    1
FROM specify_taxon_staging s
LEFT JOIN taxa t
    ON t.sp_taxonID = s.sp_taxonID
   AND t.sp_institutionID = 1
WHERE t.id IS NULL;