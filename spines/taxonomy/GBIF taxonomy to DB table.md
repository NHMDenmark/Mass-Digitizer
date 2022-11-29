### This staatement prepares the table to be imported into. The fields are generally large in order to accomodate the largest strings in the GBIF taxonomy. The 'namepublishedin' column can on occation be very large.

```

CREATE TABLE public.gbif2022 (
	taxonid text NULL,
	datasetid varchar(512) NULL,
	parentnameusageid text NULL,
	acceptednameusageid varchar(512) NULL,
	originalnameusageid varchar(512) NULL,
	scientificname varchar(512) NULL,
	scientificnameauthorship varchar(512) NULL,
	canonicalname varchar(512) NULL,
	genericname varchar(512) NULL,
	specificepithet varchar(512) NULL,
	infraspecificepithet varchar(512) NULL,
	taxonrank varchar(512) NULL,
	nameaccordingto varchar(512) NULL,
	namepublishedin varchar(2048) NULL,
	taxonomicstatus varchar(512) NULL,
	nomenclaturalstatus varchar(512) NULL,
	taxonremarks varchar(512) NULL,
	kingdom varchar(512) NULL,
	phylum varchar(512) NULL,
	class_ varchar(512) NULL,
	order_ varchar(512) NULL,
	"family" varchar(512) NULL,
	genus varchar(512) NULL,
	taxonomic_source varchar(128) NULL
);
``` 
Having this table at hand is useful for fast GBIF lookups. Of course you lose the wonderful ElasticSearch functionality which GBIF supplies.
