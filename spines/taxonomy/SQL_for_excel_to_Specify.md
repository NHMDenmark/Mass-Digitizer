I am a little foggy about this one, but as I recall it is meant to create a table structured according to a spreadsheet document and that would make it digestable for Specify down the line.



--############CONFORM TO EXCEL STRUCTURE  

--##Prep for excel sheet structure  
```
CREATE TABLE excel_conformant (
id int generated always as identity,
"DOMAIN"  varchar(64),
kingdom varchar(64), 
subkingdom  varchar(64),
division  varchar(64), 
subdivision  varchar(64),
"class"  varchar(64),
subclass  varchar(64), 
superorder  varchar(64), 
"ORDER"  varchar(64), 
suborder  varchar(64),
"FAMILY"  varchar(64),
genus  varchar(64),
species  varchar(64), 
subspecies  varchar(64), 
variety  varchar(64), 
forma  varchar(64), 
subforma  varchar(64),
parent_of_taxon varchar(64),
col_status  varchar(64),
preferred_taxon  varchar(64),
is_preferred_q  varchar(64),
common_name  varchar(64),
is_hybrid  varchar(64),
author  varchar(128), 
"source"  varchar(64),
Taxonomic_Serial_Number  int,
Hybrid_Parent1  varchar(64), 
Hybrid_Parent2  varchar(64),
remarks  varchar(256), 
GUID  varchar(64)
);

--


ALTER TABLE final_taxonomy_for_specify  ALTER COLUMN id SET DEFAULT nextval('the_serial');

INSERT INTO excel_conformant2000 ("DOMAIN", kingdom, subkingdom, division, subdivision, "class", subclass, superorder, "ORDER", suborder, "FAMILY", genus  ,species  , subspecies  , variety  , forma  , subforma  ,parent_of_taxon ,col_status  ,preferred_taxon  ,is_preferred_q  ,common_name  ,is_hybrid  ,author  , "source"  ,Taxonomic_Serial_Number,Hybrid_Parent1  , Hybrid_Parent2  ,remarks  , GUID)
SELECT f."domain" ,f.kingdom, COALESCE(NULLIF(f.subkingdom ,'')),f.division ,COALESCE(NULLIF(f.subdivision, '')) , f."class", COALESCE(NULLIF(f.subclass, '')), NULL, f."order", COALESCE(NULLIF(f.suborder,'')) , f."family",
f.genus , f.species , COALESCE(NULLIF(f.subspecies,'')) , f.variety , f.forma , f.subforma , f.parent_of_taxon , f.col_status , f.preferred_taxon , f.is_preferred,
f.common_name ,f.is_hybrid , f.author , f."source" , cast(coalesce(nullif(f.taxonomic_serial_number,''),'0') as float) , f.hybrid_parent1 , f.hybrid_parent2, f.remarks , f.guid  FROM final_taxonomy_for_specify f;
```
