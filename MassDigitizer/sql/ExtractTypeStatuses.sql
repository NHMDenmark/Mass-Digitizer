  -- To be run on Specify database for each collection 
  	SELECT -- pli.* -- pli.Title  -- pli.PickListItemID, pli.Value, pli.Title    
			 CONCAT (',(', pli.PickListItemID, ',"', pli.Title, '","', pli.Value , 
			 '", (SELECT id FROM collection WHERE spid = ', pl.CollectionID, 
			 ' AND institutionid = 1))') -- Adjust institutionid : NHMD - 1, NHMA - 2 
			 sqlstatement 
 FROM picklist pl 
 	JOIN picklistitem pli ON pli.PickListID = pl.PickListID 
 		WHERE pl.Name = 'TypeStatus' AND pl.CollectionID = 0 -- Adjust collection id :  
															 --    NHMD Tracheophyta - 688130 
 		ORDER BY pli.Ordinal;
