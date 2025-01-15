use `dassco-au`;

SELECT 
    s.barcode,
    s.id AS specimen_id,
    s.guid,
    s.digitiser,
    s.date_asset_taken,
    s.folder_id,
    f.id AS folder_version_id,
    f.area,
    f.gbif_match_json,
    f.created_at
FROM specimen s
LEFT JOIN (
    SELECT fv.*
    FROM folder_versions fv
    INNER JOIN (
        SELECT folder_id, MAX(created_at) AS max_created_at
        FROM folder_versions
        GROUP BY folder_id
    ) AS max_fv ON fv.folder_id = max_fv.folder_id AND fv.created_at = max_fv.max_created_at
) f ON s.folder_id = f.folder_id
WHERE s.date_asset_taken >= '2024-10-10'
-- AND f.gbif_match_json IS NOT NULL
AND f.gbif_match_json != 'null';