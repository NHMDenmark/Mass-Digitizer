# Steps in the post processing script
The refine tool used here is OpenRefine.


The digitization files come in CSV format and they have to be imported into the Open Refine tool.

 The following columns 'taxonspid' and 'rankid' are converted to numerical data columns that import as text formatted data, these need to be converted to numerical because there are GREL code that tests on the assumption that numbers are numbers. GREL code con be obtained here: https://github.com/NHMDenmark/Mass-Digitizer/blob/main/OpenRefine/post_processing.json   
 
 - Text transform on cells in column rankid using expression `value.toNumber()`  
 - Text transform on cells in column taxonspid using expression `value.toNumber()`

We check to see if the value "None" appears in taxonspid.
- Text transform on cells in column taxonspid using expression `if((value==null).or(value==0).or(value=='None'), '', value)`

A new column 'newtaxonflag' is created is derived from the 'taxonspid' field:  
- Create column newtaxonflag at index 11 based on column taxonspid using expression 
    - `if((value==null).or(value==0), 'True', 'False')`
 

The storagefullname column is split by separator so that we can have the storage property in atomic units.  
- `"Split column storagefullname by separator"` The separator here is " | " (notice the leading and trailing whitespace)  
- `"Remove column storagefullname 1"` This is the institution column that we are not mapping.
- `"Rename column storagefullname 2 to site"`  
- `"Rename column storagefullname 3 to collection"` 


At this point a 'shelf' column and a 'box' column is created. This is specific for NHMD Vascular Plants which has shelves and boxes. 
- Create column shelf based on column storagename using expression `if(value.split(' ')[0] == 'Shelf', value.split(' ')[1], '')`  
- Create column box based on column storagename using expression `if(value.split(' ')[0] == 'Box', value.split(' ')[1], '')`

In case there are [name sp.] taxon values in fullname, then these need to be marked up in a qualifier column.
- Create column qualifier at index 5 based on column taxonfullname using expression `if(value.contains(" sp. "), 'sp.', '')`

The following steps create the taxonomy levels and assign values to them based on the rank ID.  

- Create column genus based on column taxonfullname using expression `if(cells['rankid'].value >= 180, value.split(' ')[0], '')`  
- Create column species based on column taxonfullname using expression `if(cells['rankid'].value >= 220, value.split(' ')[1], '')`  
- Create column subspecies based on column taxonfullname using expression `if(cells['rankid'].value == 230, value.split(' ')[2], '')`  
- Create column variety based on column taxonfullname using expression `if(cells['rankid'].value == 240, value.split(' ')[3], '')`  
- Create column forma at on column taxonfullname using expression `if(cells['rankid'].value == 260, value.split(' ')[3], '')`  


In order to identify new taxon ranks we have to add new[ *taxonRank* ] flags to the code.  
- Create column newgenusflag based on column genus using expression:
    - `if((cells['newtaxonflag'].value=='True').and(cells['rankid'].value == 180), 'True', '')`  
- Create column newspeciesflag based on column taxonfullname using expression:
    - `if((cells['newtaxonflag'].value=='True').and(cells['taxonfullname'].value == 220, 'True',  '')`  
- Create column newsubspeciesflag based on column newtaxonflag using expression: 
    - `if((cells['newtaxonflag'].value=='True').and(cells['taxonfullname'].value == 230), 'True',  '')`  
- Create column newvarietyflag based on column newtaxonflag using expression:
    - `if((cells['newtaxonflag'].value=='True').and(cells['taxonfullname'].value == 240), 'True',  '')`  
- Create column newformaflag based on column taxonfullname using expression: 
    - `if((cells['newtaxonflag'].value=='True').and(cells['rankid'].value==260), 'True',  '')`


- Rename column familyname to family
- Rename column multispecimen to container  
- Rename column georegionname to broadgeographicalregion  


The broadgeographicalregion is duplicated into a column named 'localityname'.  
- Create column localityname based on column georegionname using expression grel:value  
Workbench will fail validation if this element is not here.


The agentMiddleInitial is checked and corrected if the value is 'None'

The column 'catalogeddate' is needed and must be created from a timestamp column 'recordeddatetime' which requires these steps:  
- Create column catalogeddate based on column recorddatetime using expression `value.slice(0,10)`  
- Text transform on cells in column catalogeddate using expression `value.toDate()`  
- Text transform on cells in column catalogeddate using expression `value.toString('dd/MM/yyyy')`  

There will be two columns for ready-to-publish and project-name:
- A novel column is made with the name 'publish' and the value 'True' signifying that the records are ready for publishing to GBIF.
- Another column is needed: 'project' which contains the name 'DaSSCo'. This will make it easier to find records from the DaSSCo project.



The hybrids will be caught:
- Text transform on cells in column species using expression `if(cells['genus'].value.contains(\" x \"), cells['genus'].value, value)`

Format container by removing the prepended apostrophe:
- Text transform on cells in column container using expression `if(value.startsWith(\"'\"), value.replace(\"'\", ''), '')`

The term "sp." is removed from the species column. 
- `if(value.contains('sp.'), '', value)` 

Populate the qualifier column with qualifiers aff. or cf.
- `if(value.contains("aff\."), 'aff.', value)`
- `if((value.contains("cf\."), 'cf.', value)`

Remove the qualifiers aff. or cf. in the species field if any show up.
- `if((value.contains("aff\.").or(value.contains("cf\."))), '', value)`

#### Lastly reorder the column names to your liking

## Columns that are removed:

* ID
* spid
* taxonnameid  
* taxonspid
* rankid
* Typestatusid
* georegionid
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
For collections that do not have 'box' or 'shelf' these two columns can also be removed.
## Final step: Export
The refined file must be exported as "Windows 1252: Western European" encoded to allow for characters outside the ANSI spectrum.
