UPDATE taxa
SET dassco_fullname = CONCAT(dassco_name, ' ', dassco_author)
WHERE dassco_rankid >= 220
  AND COALESCE(dassco_author,'') <> ''
  AND dassco_fullname = dassco_name;
