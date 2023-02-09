  -- To be run on Specify database for each collection 
  	SELECT    
	CONCAT (',(', st.StorageID, ',"', st.Name, , ',"', st.Name, 
            '", (SELECT id FROM collection WHERE spid = ', pt.CollectionID, 
		    ' AND institutionid = 1))') -- Adjust institutionid : NHMD - 1, NHMA - 2  
	sqlstatement 
 FROM storage st 
 		 