This particular taxonomy did not have discrete Species names, so it had to be lifted from the binomial. (Column shortname contains the binomial)

```
SELECT a.shortname AS taxonfullname, reverse(split_part(reverse(a.shortname),' ',1)) AS name, 
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
ELSE NULL END AS "rank",
13 AS taxontreedefid,
st.lowest_taxonid AS taxonid,
st."Class" AS classid
FROM aarhus a LEFT JOIN specify_taxonomy st ON st.taxonfullname = a.shortname ;
```

