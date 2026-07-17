DROP TABLE IF EXISTS taxon;

CREATE TABLE taxon (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,

    dassco_taxonID               CHAR(32) NOT NULL,

    dassco_name                  VARCHAR(512) NULL,
    dassco_author                VARCHAR(256) NULL,
    dassco_fullname              VARCHAR(1024) NULL,
    dassco_epithet               VARCHAR(128) NULL,
    dassco_rankid                CHAR(3) NULL,
    dassco_extinct               VARCHAR(5) NULL,

    dwc_taxonID                  VARCHAR(32) NULL,
    dwc_scientificName           VARCHAR(1024) NULL,
    dwc_scientificNameAuthorship VARCHAR(256) NULL,

    dwc_parentNameUsageID        VARCHAR(32) NULL,
    dwc_parentNameUsage          VARCHAR(512) NULL,

    dwc_acceptedNameUsageID      VARCHAR(32) NULL,
    dwc_acceptedNameUsage        VARCHAR(512) NULL,

    dwc_taxonomicStatus          VARCHAR(64) NULL,
    dwc_taxonRank                VARCHAR(32) NULL,

    sp_taxonID                   VARCHAR(32) NULL,
    sp_fullname                  VARCHAR(1024) NULL,
    sp_author                    VARCHAR(256) NULL,
    sp_rankid                    CHAR(3) NULL,
    sp_rankname                  VARCHAR(32) NULL,
    sp_parentname                VARCHAR(512) NULL,
    sp_taxonnr                   VARCHAR(32) NULL,
    sp_taxonnrsource             VARCHAR(128) NULL,
    sp_taxontreedefid            INT NULL,

    PRIMARY KEY (id),

    KEY idx_dassco_taxonID (dassco_taxonID),
    KEY idx_dwc_taxonID (dwc_taxonID),
    KEY idx_sp_taxonID (sp_taxonID),

    KEY idx_dwc_parentNameUsageID (dwc_parentNameUsageID),
    KEY idx_dwc_acceptedNameUsageID (dwc_acceptedNameUsageID)

) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;