 SELECT co.collectionobjectid, co.catalognumber, co.projectnumber, co.collectingeventid, d.DeterminationID, t.FullName, p.PrepTypeID, c.CollectionName, co.CreatedByAgentID, a.FirstName
 	FROM collectionobject co 
	LEFT JOIN determination d ON d.CollectionObjectID = co.collectionobjectid
	LEFT JOIN taxon t ON t.TaxonID = d.DeterminationID
	LEFT JOIN collection c ON c.collectionId = co.CollectionID
	LEFT JOIN preparation p ON p.CollectionObjectID = co.CollectionObjectID
	LEFT JOIN agent a ON a.AgentID = co.CreatedByAgentID 
-- DELETE FROM collectionobject 
	WHERE  
 	   ProjectNumber IN ('Reserved for DaSSCo', 'Mass digitization init', 'Exh. Pollinating beetles 3.7D.2', 'Reserved for båndfluesamling', 'Pinned Insects') AND 
/*			(
			   catalogNumber BETWEEN xxx AND xxx 
			 ) 
*/
		 catalogNumber IN (
		 000
		 )
		 LIMIT 5000;
 	      