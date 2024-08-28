 DELETE FROM collectionobject 
-- SELECT collectionobjectid, catalognumber, projectnumber FROM collectionobject 
	WHERE (ProjectNumber = 'Reserved for DaSSCo' OR ProjectNumber = 'Exh. Pollinating beetles 3.7D.2')  
	 		AND 
			(
				catalogNumber BETWEEN 1152213 AND 1152310 OR
				catalogNumber BETWEEN 1152312 AND 1152443 OR
				catalogNumber BETWEEN 1152445 AND 1152970 OR
				catalogNumber BETWEEN 1152971 AND 1153050 OR
				catalogNumber BETWEEN 1153073 AND 1153364 OR
				catalogNumber BETWEEN 1153524 AND 1153528 OR
				catalogNumber BETWEEN 1153932 AND 1154000 OR
				catalogNumber BETWEEN 1154001 AND 1154069 OR
				catalogNumber BETWEEN 1154681 AND 1155928 OR
				catalogNumber BETWEEN 1155929 AND 1156062 OR
				catalogNumber BETWEEN 1156064 AND 1156476 OR
				catalogNumber BETWEEN 1156477 AND 1156727 OR
				catalogNumber BETWEEN 1156729 AND 1156761 OR
				catalogNumber BETWEEN 1156763 AND 1156921 OR
				catalogNumber BETWEEN 1156926 AND 1157061 OR
				catalogNumber BETWEEN 1157063 AND 1157194 OR
				catalogNumber BETWEEN 1157196 AND 1157351 OR
				catalogNumber BETWEEN 1157353 AND 1157460 OR
				catalogNumber BETWEEN 1157462 AND 1157563 OR
				catalogNumber BETWEEN 1157567 AND 1157573 OR
				catalogNumber BETWEEN 1157576 AND 1157626 OR
				catalogNumber BETWEEN 1157628 AND 1157646 OR
				catalogNumber BETWEEN 1157648 AND 1157652 OR
				catalogNumber BETWEEN 1157654 AND 1157700 OR
				catalogNumber BETWEEN 1157702 AND 1157799 OR
				catalogNumber BETWEEN 1157802 AND 1158077 OR
				catalogNumber BETWEEN 1158078 AND 1158187 OR
				catalogNumber = 1150554 OR
				catalogNumber = 1150897 OR
				catalogNumber = 1152444 
			 ) 
	      ;
	      