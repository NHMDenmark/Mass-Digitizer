DROP TABLE IF EXISTS taxon_rank;

CREATE TABLE taxon_rank (
    dwc_taxonRank VARCHAR(32) NOT NULL,
    dassco_rankid CHAR(3) NOT NULL,

    PRIMARY KEY (dwc_taxonRank),
    KEY idx_dassco_rankid (dassco_rankid)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;
  
INSERT INTO taxon_rank (dwc_taxonRank, dassco_rankid)
VALUES
    ('life',         '000'),
    ('kingdom',      '010'),
    ('subkingdom',   '020'),
    ('phylum',       '030'),
    ('division',     '030'),
    ('subphylum',    '040'),
    ('subdivision',  '040'),
    ('superclass',   '050'),
    ('class',        '060'),
    ('subclass',     '070'),
    ('infraclass',   '080'),
    ('superorder',   '090'),
    ('order',        '100'),
    ('suborder',     '110'),
    ('infraorder',   '120'),
    ('superfamily',  '130'),
    ('family',       '140'),
    ('subfamily',    '150'),
    ('tribe',        '160'),
    ('subtribe',     '170'),
    ('genus',        '180'),
    ('subgenus',     '190'),
    ('species group','200'),
    ('species',      '220'),
    ('subspecies',   '230'),
    ('variety',      '240'),
    ('subvariety',   '250'),
    ('forma',        '260'),
    ('subforma',     '270');  