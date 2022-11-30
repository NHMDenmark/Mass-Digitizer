# The Taxonomy building process

Here are some observations and suggested methods based on the experience gained from the Botanical taxonomy building project.
## Initially
There should be a prioritized list of taxonomy spines for ingestion into the end spine for the relevant discipline. (IE. The taxon product we will end up matching specimen names against).
1.	Local taxonomies that are in use. Their names are likely to be present on the collection specimen labels. The Specify taxonomy being an obvious component.
2.	Decide which columns there should be in the spine! Specify will likely dictate this as it is the ultimat recipient of the taxonomy.
3.	Authoritative taxonomies that are widely accepted, such as Catalog of Life, CoL , or low hanging fruits like the GBIF taxonomy, which contains: National checklist of all species occurring in Denmark, ITIS, Dyntaxa, etc. Many checklists not mentioned here will already be present in the GBIF backbone.
4.	Ask curators and local taxonomy experts for checklists and recommendations.
5.	Make sure to always add a column “taxonomic_source” that states which checklist the added records hail from. Like ‘Specify’ or ITIS or ‘Dyntaxa’.

## Process
Initially one checklist is uploaded to the developer database. The GBIF taxonomy would be a good place to start. Personally, I am using Postgres as it has a great palette of SQL tools with which to clean and manipulate data.
The addition of new spines will result in a specific number of DB records. This number should steadily grow as more spines are added. This is a simple check to perform.
Important: Clean each spine before making any joins or mergers with the development taxonomic spine! Having to step back in the dev spine is a pain in the ace.
Import each spine (after cleaning) into its own table in the dev DB. After each new spine is joined to the dev spine: A “unit test” should be run to see if what is expected is there!
1.	Unit test could be a number-of-records check
2.	Or a list of names check
3.	Duplicates check
4.	Did we lose any names since last iteration?
5.	All of the above
This should be scripted in Python for easy initiation and completeness.

Ongoing testing
There should be a versioning system in place so that taxonomy versions could be compared to each other. This would satisfy /Process-imprimis “number-of-records” check.
 
## Sequence
0. Create a database instance on your favorite enterprise DB system (Posrgres, MySQL/Maria, MSSQL, Oracle, ...)
1. Draw out the Specify taxonomy using the "Specify_translator_SQL" that you can find here: https://github.com/NHMDenmark/DaSSCo/blob/main/spines/taxonomy/translator%20of%20Specify%20MySQL%20taxon%20table.md
Import this dataset into a table in the DB instance giving it a suitable name. **Important** - Make sure to add a column with the default value of the source name.  Now you have one of the cornerstones for the taxonomic spine product.
2. Create another table 
