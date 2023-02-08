  -- To be run on Specify database for each collection 
  	SELECT    
	CONCAT (',(', pt.PrepTypeID, ',"', pt.Name, '", (SELECT id FROM collection WHERE spid = ', pt.CollectionID, 
		    ' AND institutionid = 1))') -- Adjust institutionid : NHMD - 1, NHMA - 2  
	sqlstatement 
 FROM preptype pt 
 		WHERE pt.CollectionID = 0 
		-- Adjust collection id : 
		--    NHMD Tracheophyta - 688130 
		-- 	  NHMD Entomology - 163841
		--    NHMA Entomology - 2 