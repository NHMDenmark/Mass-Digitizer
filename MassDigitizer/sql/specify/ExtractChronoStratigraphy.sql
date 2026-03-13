SELECT 
	-- INSERT INTO chronostratigraphy (spid, name, fullname, parentfullname, collectionid, treedefid, rankname, rankid) VALUES 
	-- g.GeologicTimePeriodID, g.Name, g.FullName, g.RankID, g.ParentID,
	CONCAT('(', g.GeologicTimePeriodID, ',"', -- spid
	            g.Name, '","',                -- name
					g.FullName, '",',             -- fullname 
					p.FullName,                   -- parentfullname  
					',(SELECT id FROM collection WHERE spid = 327682 AND institutionid = 1)),', g.ParentID,'),',
					g.GeologicTimePeriodTreeDefID, -- treedefid 
					r.Name                         -- rankname 
					g.RankID                       -- rankid
					)
	FROM geologictimeperiod g 
	LEFT JOIN geologictimeperiod p ON p.GeologicTimePeriodID = g.parentID
	LEFT JOIN geologictimeperiodtreedefitem r ON r.GeologicTimePeriodTreeDefItemID = g.GeologicTimePeriodTreeDefItemID 
	WHERE g.GeologicTimePeriodTreeDefID = 1;