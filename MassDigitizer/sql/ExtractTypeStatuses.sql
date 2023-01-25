  -- To be run on Specify database for each collection 
  	SELECT pli.* -- , -- pli.Title  -- pli.PickListItemID, pli.Value, pli.Title    
 FROM picklist pl 
 	JOIN picklistitem pli ON pli.PickListID = pl.PickListID 
 		WHERE pl.Name = 'TypeStatus' AND pl.CollectionID = 32769 -- Adjust collection id :  
															              --    NHMD Tracheophyta - 688130 
																		  --	NHMD Entomology   - 163841
															              --    NHMA Entomology   - 32769
											  AND pli.Title NOT LIKE 'Ex %'
											  AND pli.Value NOT LIKE '%yyy%'
 		ORDER BY pli.Ordinal;