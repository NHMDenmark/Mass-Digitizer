DROP TABLE IF EXISTS institution;

CREATE TABLE institution (
    institutionID INT NOT NULL,
    code VARCHAR(16) NOT NULL,
    name VARCHAR(255) NOT NULL,
    url VARCHAR(255) NULL,
    visible BOOLEAN NOT NULL DEFAULT TRUE,

    PRIMARY KEY (institutionID),
    UNIQUE KEY uq_institution_code (code)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=UTF8MB4_GENERAL_CI;

ALTER TABLE taxa
ADD COLUMN sp_institutionID INT NULL
AFTER sp_taxontreedefid;

CREATE INDEX idx_sp_institutionID
ON taxa (sp_institutionID);


INSERT INTO institution (
    institutionID,
    code,
    name,
    url,
    visible
)
VALUES
    (1,  'NHMD',  'Natural History Museum of Denmark',           'https://specify-snm.science.ku.dk/',      TRUE),
    (2,  'NHMA',  'Natural History Museum Aarhus',               'https://specify-nhma.science.ku.dk/',     TRUE),
    (3,  'AU',    'Aarhus University Herbarium',                'https://specify-test.science.ku.dk/',     FALSE),
    (4,  'MMG',   'Museum Mors & Fur Museum',                   'https://specify-muserum.science.ku.dk/',  FALSE),
    (5,  'FIMUS', 'Fiskeri- og Søfartmuseet',                   'https://specify-fimus.science.ku.dk/',    FALSE),
    (6,  'MSJN',  'Museum Sønderjylland (Gram)',                'https://specify-msjn.science.ku.dk/',     FALSE),
    (7,  'S',     'Naturama',                                   'https://specify-naturama.science.ku.dk/', FALSE),
    (8,  'OESM',  'Østsjællands Museum (Faxe)',                 'https://specify-oesm.science.ku.dk/',     FALSE),
    (99, 'TEST',  'Test Institution',                           'https://specify-test.science.ku.dk/',     FALSE);
