SELECT
    CONCAT(
        "(",
        COALESCE(sp_taxonID, 0), ",",
        COALESCE(dwc_taxonID,0), ",'",

        REPLACE(COALESCE(dassco_taxonID, ""), "'", "''"), "','",

        REPLACE(COALESCE(dassco_name, ""), "'", "''"), "','",

        REPLACE(COALESCE(dassco_author, ""), "'", "''"), "','",

        REPLACE(COALESCE(dassco_fullname, ""), "'", "''"), "',",

        COALESCE(dassco_rankid, "0"), ",'",

        CASE dassco_rankid
            WHEN '010' THEN 'Kingdom'
            WHEN '030' THEN 'Phylum'
            WHEN '060' THEN 'Class'
            WHEN '100' THEN 'Order'
            WHEN '140' THEN 'Family'
            WHEN '180' THEN 'Genus'
            WHEN '190' THEN 'Subgenus'
            WHEN '220' THEN 'Species'
            WHEN '230' THEN 'Subspecies'
            WHEN '240' THEN 'Variety'
            WHEN '250' THEN 'Subvariety'
            WHEN '260' THEN 'Forma'
            ELSE ''
        END,

        "','",

        REPLACE(
            COALESCE(sp_parentname, dwc_parentNameUsage, ""),
            "'",
            "''"
        ),

        "','",

        REPLACE(
            COALESCE(dwc_acceptedNameUsage, ""),
            "'",
            "''"
        ),

        "',",

        COALESCE(sp_taxontreedefid, 0),

        ",",

        COALESCE(sp_institutionID, 0),

        ",'",

        REPLACE(
            COALESCE(sp_taxonnr, ""),
            "'",
            "''"
        ),

        "','",

        REPLACE(
            COALESCE(sp_taxonnrsource, ""),
            "'",
            "''"
        ),

        "'),"
    ) AS sqlstatement
    
FROM taxa
WHERE 
       dassco_rankid <= '190' -- Highertaxa
      -- dassco_rankid = '220'  -- Species 
      -- AND dassco_fullname NOT LIKE '% x %' AND dassco_fullname NOT LIKE '% × %' AND dassco_fullname NOT LIKE 'x %' AND dassco_fullname NOT LIKE '× %' -- leave out Hybrids
      -- dassco_rankid = '230'  -- Subspecies 
      -- dassco_rankid > '230'  -- VarForma
ORDER BY dassco_fullname

 LIMIT  350000 OFFSET 
             0 -- File 1
      --  350000 -- File 2
      --  700000 -- File 3 
      -- 1050000 -- File 4
;