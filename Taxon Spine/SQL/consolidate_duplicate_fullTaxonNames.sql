#Let us say that we have created a table based on TaxonSpine_Tracheophyta.sql, and we have imported this into a PostgresQL DB (for reasons to do with 'similarity', 'Levenschtein distance' and other string comparisons that MySQL does not have)
#We then do a simple COUNT GROUP BY taxonfullname. We make sure to keep old lowest taxon IDs to be able to reconnect to collection objects in Specify later. 

SELECT t1.taxonfullname as t1full , string_agg(t1.lowest_taxonid::text, ',' order by t1.lowest_taxonid) as low_taxonIDs, count(*) as cnt
FROM specify_taxonomy  t1 
group by 1 having count(*) > 1;
