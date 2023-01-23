  -- To be run on Specify database for each collection 
  	SELECT    
	CONCAT (',(', pt.PrepTypeID, ',"', pt.Name, '", (SELECT id FROM collection WHERE spid = ', pt.CollectionID, '))') sqlstatement 
 FROM preptype pt 
 		WHERE pt.CollectionID = 0 
		-- Adjust collection id : 
		--    NHMD Tracheophyta - 688130 