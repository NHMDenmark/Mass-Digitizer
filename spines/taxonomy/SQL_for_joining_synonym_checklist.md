 #  Join synonyms (Synonymic Checklists of the Vascular Plants of the World) and The World Checklist of Vascular Plants (POWO) together: Creating a more comprehensive spine that also catches synonyms.
# The largest heading
SELECT  * FROM 
(SELECT p.taxon_name AS taxon_full_name, p."rank" AS rank_, p.authors ,p.status, 'powo_u' AS source_left FROM powo_union p)t1
LEFT JOIN 
(SELECT s.taxon_full_name , s.rank_ , s.author AS authors, s.status, 'syno' AS source_right FROM syno_prod s)t2
ON t1.taxon_full_name = t2.taxon_full_name;
