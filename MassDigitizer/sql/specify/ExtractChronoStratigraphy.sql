SELECT 
	-- INSERT INTO chronostratigraphy (spid, name, fullname, parentfullname, collectionid, treedefid, rankname, rankid) VALUES 
	CONCAT('(', g.GeologicTimePeriodID, ',"',           -- spid
	            g.Name, '","',                          -- name
					g.FullName, '","',                      -- fullname 
					p.FullName, '",',                       -- parentfullname  
					'(SELECT id FROM collection WHERE spid = 327682 AND institutionid = 1),', 
					g.GeologicTimePeriodTreeDefID, ',"',    -- treedefid 
					r.Name, '",' ,                          -- rankname 
					g.RankID, '),'                           -- rankid
					) AS SQL_statement
	FROM geologictimeperiod g 
	LEFT JOIN geologictimeperiod p ON p.GeologicTimePeriodID = g.parentID
	LEFT JOIN geologictimeperiodtreedefitem r ON r.GeologicTimePeriodTreeDefItemID = g.GeologicTimePeriodTreeDefItemID 
	WHERE g.GeologicTimePeriodTreeDefID = 1 AND g.Name <> 'Root'
	AND g.GeologicTimePeriodID IN (36,40);