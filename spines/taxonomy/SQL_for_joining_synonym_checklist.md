# Join synonyms (Synonymic Checklists of the Vascular Plants of the World) and The World Checklist of Vascular Plants (POWO) together: Creating a more comprehensive spine that also catches synonyms.

```
SELECT * FROM 
(SELECT p.taxon_name AS taxon_full_name, p."rank" AS rank_, p.authors ,p.status, 'powo_u' AS source_left FROM powo_union p)t1
LEFT JOIN 
(SELECT s.taxon_full_name , s.rank_ , s.author AS authors, s.status, 'syno' AS source_right FROM syno_prod s)t2
ON t1.taxon_full_name = t2.taxon_full_name; 
```
This query does not extract all data, since we won't get the full taxon rank 'tree', yet there is enough data to be able to join on another table containing the full taxonomic hierarchy we desire.  
Note that the 'LEFT JOIN' signifies that the table POWO (and by extension the source) is primary in this query.  

If the tables have the same columns, then it might make sense to use UNION or UNION ALL to merge the tables. UNION will merge the two tables and remove duplicates, which means it is slower than the UNION ALL statement which doesn't deal with duplicates at all.
