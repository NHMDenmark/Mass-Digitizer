# Post-processing of DaSSCo digitisation data


Post-processing is done in OpenRefine using a GREL script.

The post-processing protocol can be found here:
[Post-processing protocol](https://github.com/NHMDenmark/Mass-Digitizer/blob/main/documentation/postProcessing/import_protocol_postProcessing.md#post-processing)

The newest version of the GREL script can be found here:
[Post-processing script](https://github.com/NHMDenmark/Mass-Digitizer/blob/main/OpenRefine/post_processing.json)

Below you will find information on the steps performed by the GREL script.

### GREL script steps

1. Columns "taxonspid" and "rankid" are imported as text formatted data and need to be converted to numerical because there are GREL code that tests on the assumption that numbers are numbers:   
 
	- Text transform on cells in column taxonspid using expression `value.toNumber()`
 
	- Text transform on cells in column rankid using expression `value.toNumber()`

2. To correctly work with hybrids, a new column called ishybrid is added and set to True for all rows where taxonfullname includes "x ":

	- Create column ishybrid at index 4 based on column taxonfullname using expression `grel:if(value.contains(\"x \"), \"True\", \"False\")`

3. For the taxonomy to be mapped correctly in Specify, the taxonomic information in column "taxonfullname" need to be split up into separate columns for qualifier, genus, species, subspecies, variety and forma:
	
	Column "qualifier" is created based on column "taxonfullname" and populated with qualifier specific values:
	
	- Create column qualifier at index 5 based on column taxonfullname using expression `grel:if(value.contains(' sp. '), 'sp.', '')`
	
	- Text transform on cells in column qualifier using expression `grel:if(cells['taxonfullname'].value.contains('aff.'), 'aff.', value)`
	
	- Text transform on cells in column qualifier using expression `grel:if(cells['taxonfullname'].value.contains('cf.'), 'cf.', value)` 

	Columns for several taxonomic levels are created based on column "taxonfullname" and populated with values based on rankID:
	
	- Create column genus at index 5 based on column taxonfullname using expression `grel:if(cells['rankid'].value >= 180, value.split(' ')[0], '')`
	
	- Create column species at index 5 based on column taxonfullname using expression `grel:if(cells['rankid'].value >= 220, if(cells['ishybrid'].value == 'True', forEach(value.split(' '), w, if(startsWith(w, toLowercase(w)), w, '')).join(' ').trim(), value.split(' ')[1]), '')`
	
	- Create column subspecies at index 5 based on column taxonfullname using expression `grel:if(cells['rankid'].value == 230, value.split(' ')[2], '')`
	
	- Create column variety at index 5 based on column taxonfullname using expression `grel:if(cells['rankid'].value == 240, cells['taxonfullname'].value.split(' ')[-1], '')`

	- Create column forma at index 5 based on column taxonfullname using expression `grel:if(cells['rankid'].value == 260, value.split(' ')[3], '')`

	The term "sp." is removed from the "species" column:
	
	- Text transform on cells in column species using expression `grel:if(value=='sp.', '', value)`

4. The different types of null values in column "taxonspid" need to be standardised because it is used as a condition in the creation of another column:
	- Text transform on cells in column taxonspid using expression `grel:if((value==null).or(value==0).or(value=='None').or(value==''), '', value)`

5. We want to mark new taxon records that will be added to the taxon tree in Specify when importing so they can be checked.
	
	First, column "newtaxonflag" is created based on column "taxonspid" and is populated with "True" or "False" depending on whether or not the taxon has a taxonspid:

	- Create column newtaxonflag at index 18 based on column taxonspid using expression `grel:if((value==null).or(cells['taxonspid'].value==''), 'True', 'False')`

	Then individual newtaxonflag columns are created for all taxonomic levels based on the values in the newly created "newtaxonflag" column and the rankID:

	- Create column newgenusflag at index 5 based on column taxonfullname using expression `grel:if((cells['newtaxonflag'].value=='True').and(cells['rankid'].value == 180), 'True', '')`

	- Create column newspeciesflag at index 5 based on column taxonfullname using expression `grel:if((cells['newtaxonflag'].value=='True').and(cells['rankid'].value == 220), 'True', '')`

	- Create column newsubspeciesflag at index 5 based on column taxonfullname using expression `grel:if((cells['newtaxonflag'].value=='True').and(cells['rankid'].value==230), 'True', '')`
	
	- Create column newvarietyflag at index 5 based on column taxonfullname using expression `grel:if((cells['newtaxonflag'].value=='True').and(cells['rankid'].value==240), 'True', '')`

	- Create column newformaflag at index 5 based on column taxonfullname using expression `grel:if((cells['newtaxonflag'].value=='True').and(cells['rankid'].value==260), 'True', '')`

6. **For NHMA:** The value "None" needs to be deleted from the column "taxonnumber":
	- Mass edit cells in column taxonnumber

7. Columns "familyname" and "georegionname" are renamed:
	- Rename column familyname to family
	- Rename column georegionname to broadgeographicalregion

8. We need to create locality names for all locality records because you cannot create a locality record without it. Column "locality" is created and populated with the values from column "broadgeographicalregion":
	- Create column localityname at index 28 based on column broadgeographicalregion using expression `grel:value`

9. For the storage to be mapped correctly in Specify, the storage information in column "storagefullname" needs to be split up into separate columns. Column "storagefullname" is split by separator and columns for collection, cabinet, box, and shelf are created:
	- Split column storagefullname by separator, the separator here is "|" 

	- Create column 'collection' at index 25 based on 'storagefullname 4' (if it exists) and 'storagefullname 1' using expression `grel:if(filter([cells[\"storagefullname 1\"]], c, c.value.contains(\"Aarhus\")).length() > 0, if(filter([cells[\"storagefullname 4\"]], c, c.value != null).length() > 0, cells[\"storagefullname 4\"].value, \"\"), \"\")`

	- Text transform on cells in column collection using expression `grel:if(cells[\"storagefullname 1\"].value.contains(\"Denmark\"), cells[\"storagefullname 3\"].value, value)`
	
	- Create column box at index 21 based on column storagefullname using expression `grel:if(value.contains(\"Box\"), value.replace(/.*?Box (\\d+).*/, \"$1\"), \"\")`
	
	- Create column shelf at index 21 based on column storagefullname using expression `grel:if(value.contains(\"Shelf\"), value.replace(/.*?Shelf (\\d+).*/, \"$1\"), \"\")`

	- Create column cabinet at index 21 based on column storagefullname using expression `grel:if(value.contains(\"Cabinet\"), value.replace(/.*?Cabinet (\\d+).*/, \"$1\"), \"\")`

10. Agent name fields should either be blank or have an actual name in them, so value "None" is deleted from column "agentmiddleinitial":
	- Text transform on cells in column agentmiddleinitial using expression `grel:if(value=='None', '', value)`

11. We need to create a column for catalogeddate. Column "catalogeddate" is created based on column "recorddatetime" with values in the correct format depending on the institution:
	- Text transform on cells in column recorddatetime using expression `grel:value.slice(0,10).replace('-', '/')`
	
	**For NHMA:**
	
	- Text transform on cells in column recorddatetime using expression `grel:value.split('/')[2] + '/' + value.split('/')[1] + '/' + value.split('/')[0]`

	**For NHMD and NHMA:**

	- Create column catalogeddate at index 31 based on column recorddatetime using expression `grel:value`

	**For NHMD:**

	- Text transform on cells in column catalogeddate using expression `value.toDate()`

	- Text transform on cells in column catalogeddate using expression `grel:value.toString('yyyy-MM-dd')`

12. **For NHMD:** All records need to be marked as DaSSCo records. Column "project" is created and populated with value "DaSSCo" for all records:
	- Create column project at index 2 based on column id using expression `grel:'DaSSCo'`

13. It needs to be indicated for all records in Specify whether or not they are ready to be published to external portals, e.g. GBIF. All DaSSCo records are as default ready to be published. Column "publish" is created and populated with the value "True" for all records:
	- Create column publish at index 24 based on column id using expression `grel:'True'`

14. **For NHMA:** Individual taxonnumber and taxonnrsource columns are created for family, genus, and species based on column "taxonnumber" and facets for rankID:
	- Create column family_taxonnumber at index 28 based on column taxonnumber using expression `grel:value`

	- Create column family_taxonnrsource at index 28 based on column taxonnrsource using expression `grel:value`

	- Create column genus_taxonnumber at index 28 based on column taxonnumber using expression `grel:value`

	- Create column genus_taxonnrsource at index 28 based on column taxonnrsource using expression `grel:value`

	- Create column species_taxonnumber at index 28 based on column taxonnumber using expression `grel:value`

	- Create column species_taxonnrsource at index 28 based on column taxonnrsource using expression `grel:value`

15. Several columns are renamed to match the labels used in Specify:
	- Rename column agentfirstname to cataloger firstname

	- Rename column agentmiddleinitial to cataloger middle

	- Rename column agentlastname to cataloger lastname

	- Rename column project to projectnumber

	- Rename column notes to remarks
 
16. For the taxonomic author information to be mapped correctly in Specify, individual author columns are created for several taxonomic levels based on column "taxonauthor" and facets for rankID:
	- Create column subforma_author at index 21 based on column taxonauthor using expression `grel:value`

	- Create column forma_author at index 21 based on column taxonauthor using expression `grel:value`
 
	- Create column subvariety_author at index 21 based on column taxonauthor using expression `grel:value`

	- Create column variety_author at index 21 based on column taxonauthor using expression `grel:value`

	- Create column subspecies_author at index 21 based on column taxonauthor using expression `grel:value`

	- Create column species_author at index 21 based on column taxonauthor using expression `grel:value`
 
	- Create column genus_author at index 21 based on column taxonauthor using expression `grel:value`

17. We want to indicate in Specify which taxonomic determination the specimen is stored under in the collection. Column "storedunder" is created and populated with value "True" for all records:
	- Create column storedunder at index 1 based on column id using expression `grel:"True"`

18. We want to add metadata about the datafile to the datafile which is mapped to the DaSSCo remarks table in Specify. DaSSCo remarks table columns for "datafilename" and associated "datafile date" and "datafile source" are created:
	- Create column datafile_remark at index 1 based on column id using expression `grel:"insert filename"`
 
	- Create column datafile_date at index 1 based on column id using expression `grel:cells.catalogeddate.value`

	- Create column datafile_source at index 1 based on column id using expression `grel:"DaSSCo data file"`
 
19. We want the "labelobscured" and "specimenobscured" information mapped to the DaSSCo remarks table in Specify. DaSSCo remarks table columns for "labelobscured" and "specimenobscured" are created: 
	- Create column labelobscured_remark at index 65 based on column labelobscured using expression `grel:if(value.contains("True"),"Label obscured",null)`
 
	- Create column labelobscured_source at index 65 based on column labelobscured using expression `grel:if(value.contains("True"),"DaSSCo digitisation",null)`

	- Create column labelobscured_date at index 65 based on column labelobscured using expression `grel:if(value.contains("True"),cells.catalogeddate.value,null)`
	- Create column specimenobscured_remark at index 69 based on column specimenobscured using expression `grel:if(value.contains("True"),"Specimen obscured",null)`

	- Create column specimenobscured_source at index 69 based on column specimenobscured using expression `grel:if(value.contains("True"),"DaSSCo digitisation",null)`
 
	- Create column specimenobscured_date at index 69 based on column specimenobscured using expression `grel:if(value.contains("True"),cells.catalogeddate.value,null)`

20. A column labeled "count" is added and auto-filled with a value of 1, so Specify recognizes there is at least one specimen in the record:
	- Create column count at index 1 based on column preptypename using expression `grel:1`

21. We need the string "loco ignoto vel cult." to be removed from the remarks column and added to a new column called localitynotes: 
	- Create column localitynotes at index 27 based on column remarks using expression `grel:if(cells[\"remarks\"].value.contains(\"loco ignoto vel cult.\"), \"loco ignoto vel cult.\", cells[\"localitynotes\"].value)`
	- Text transform on cells in column remarks using expression `grel:if(cells[\"remarks\"].value.contains(\"loco ignoto vel cult.\"), \n    cells[\"remarks\"].value.replace(/\\s*;?\\s*loco ignoto vel cult\\.\\s*;?\\s*/, \"\"), \n    cells[\"remarks\"].value)`	

22. If the strings "sensu lato" or "sensu stricto" are found in the remarks column, they are removed from remarks and added to a new column called addendum:
	- Create column addendum at index 27 to include 'sensu lato' or 'sensu stricto' if they exist in remarks using expression `grel:if(cells['remarks'].value.contains('sensu lato'), 'sensu lato', if(cells['remarks'].value.contains('sensu stricto'), 'sensu stricto', cells['addendum'].value))`
	- Remove 'sensu lato' and 'sensu stricto' from remarks using expression `grel:value.replace('sensu lato','').replace('sensu stricto','').trim()`

23. The "remarks" column is mapped to the DaSSCo remarks table in Specify where it will be associated with specific date and source information. Associated "remark date" and "remark source" columns for DaSSCo remarks table are created for column "remarks": 
	- Create column remark date at index 57 based on column remarks using expression `grel:if(value != null,cells.catalogeddate.value,null)`

	- Create column remark source at index 57 based on column remarks using expression `grel:if(value != null,"DaSSCo digitisation",null)`

24. Columns are reordered and the following columns are removed:

	* ID
	* spid
	* taxonnameid  
	* taxonspid
	* rankid
	* typestatusid
	* georegionid
	* storagefullname
	* storageid
	* institutionid
	* preptypeid
	* userid
	* username
	* exportuserid
	* export
	* taxonfullname
	* taxonname
	* taxonrankname
	* institution
	* recorddatetime
	* exportdatetime
	* collectionname
	* institutionname	
