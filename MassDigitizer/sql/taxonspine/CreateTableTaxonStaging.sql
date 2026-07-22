TRUNCATE TABLE TaxonSpine.specify_taxon_staging;

INSERT INTO TaxonSpine.specify_taxon_staging (
    sp_taxonID,
    sp_taxontreedefid,
    sp_fullname,
    sp_author,
    sp_rankid,
    sp_rankname,
    sp_parentid,
    sp_parentname,
    sp_acceptedid,
    sp_taxonnr
)
SELECT
    t.TaxonID,
    t.TaxonTreeDefID,
    t.FullName,
    t.Author,
    LPAD(ttdi.RankID, 3, '0'),
    ttdi.Name,
    t.ParentID,
    p.FullName,
    t.AcceptedID,
    t.TaxonomicSerialNumber
FROM NHMD.taxon t
JOIN NHMD.taxon root ON root.TaxonID = 317961
LEFT JOIN NHMD.taxon p ON p.TaxonID = t.ParentID
JOIN NHMD.taxontreedefitem ttdi ON ttdi.TaxonTreeDefItemID = t.TaxonTreeDefItemID
WHERE t.NodeNumber BETWEEN root.NodeNumber AND root.HighestChildNodeNumber
  AND (t.YesNo2 IS NULL OR t.YesNo2 = b'0');