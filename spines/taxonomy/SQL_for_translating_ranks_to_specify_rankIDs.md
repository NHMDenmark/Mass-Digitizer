In order to make taxonomies digestable for Specify we need to translate ranks into Specify rank identifiers. Here is how to do it in a CASE statement.
The "order" rank has underscore appended becaues it is a database keyword and changing the term slightly prevents DB errors.

```
SELECT ...
CASE 
	WHEN lower(a."Rank") = 'class' THEN '60'
WHEN lower(a."Rank") = 'order_' THEN '100'
WHEN lower(a."Rank") = 'family' THEN '140'
WHEN lower(a."Rank") = 'genus' THEN '180'
WHEN lower(a."Rank") = 'species' THEN '220'
WHEN lower(a."Rank") = 'subsp.' THEN '230'
WHEN lower(a."Rank") = 'var.' THEN '240'
WHEN lower(a."Rank") = 'subvariety' THEN '250'
WHEN lower(a."Rank") LIKE 'form%' THEN '260'
ELSE NULL END AS "rank", ...
FROM aarhus a
```
The 'form' or 'forma' rank has the LIKE operator because this rank has spelling variations.
