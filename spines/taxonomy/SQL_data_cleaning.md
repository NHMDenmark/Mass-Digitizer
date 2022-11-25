Cleaning out species names having var. in them. Example "Ursinia chrysanthemoides var. geyeri"  

```
SELECT * FROM my_table t WHERE t.species like '%var.';

--Same, but for subspecies
SELECT * FROM my_table t  WHERE t.subspecies  like '% var. %';
```
When you have these unwanted names, you can use the statement in a DELETE query: `DELETE FROM my_table t WHERE t.species like '%var.';`  

Should you want to extract the _species_ and the _subspecies_ from the taxon name field, this SQL string is useful:
```
SELECT split_part(species, 'subsp.', 1) AS species, split_part(species, 'subsp.', 2) AS subspecies FROM at_last al  WHERE lower(al.species)  like '%subsp.%';
-- Example name:
-- Pyrola minor x P. rotundifolia subsp. maritima
```
-- _Other designators of interest like "subsp." are_ :
```
-- var.
-- indet.
-- sedis
```

A piece of SQL for counting words in a string:
```
SELECT array_length(regexp_split_to_array(trim(' some long text  '), E'\\W+'), 1);
```

Getting the last word in a string:
```
SELECT reverse(split_part(reverse('Pyrola minor x P. ro	tundifolia subsp. maritima'),' ',1)) AS name;
```
Changing the position integer above to 7, will yield _minor_ .

--DELETE example :
```
DELETE FROM my_table t WHERE t.species like '%indet.';
```
