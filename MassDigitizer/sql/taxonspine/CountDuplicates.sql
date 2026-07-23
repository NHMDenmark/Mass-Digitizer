SELECT
    dassco_fullname,
    COUNT(*) AS cnt
FROM taxa
GROUP BY dassco_fullname
HAVING COUNT(*) > 1
ORDER BY cnt DESC;