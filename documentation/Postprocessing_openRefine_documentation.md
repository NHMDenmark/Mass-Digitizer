# Steps in the post processing script
*Note -  I am using the term 'refine tool' to make the description  generic. The refine tool used was OpenRefine.


The digitization files come in Excel, TSV or CSV formats and have to be imported into the refine tool.

 The following columns 'taxonspid' and 'rankid' are converted to numerical data columns that import as text formatted data, these need to be converted to numerical because there are GREL code that tests on the assumption that numbers are numbers. GREL code con be obtained here: https://github.com/NHMDenmark/Mass-Digitizer/blob/main/OpenRefine/post_processing.json   
 - `"Text transform on cells in column taxonspid using expression value.toNumber()"`  
 - `"Text transform on cells in column rankid using expression value.toNumber()"`

A new column 'newtaxonflag' is created is derived from the 'taxonspid' field:  
- Create column newtaxonflag at index 11 based on column taxonspid using expression 
    - `grel:if((value==null).or(value==0), 'True', 'False')`
 

The storagefullname column is split by separator so that we can have the storage property in atomic units.  
- `"Split column storagefullname by separator"` The separator here is " | " (notice the leading and trailing whitespace)
- `"Rename column storagefullname 2 to site"`  
- `"Rename column storagefullname 3 to collection"` 
- `"Remove column storagefullname 1"` This is the institution column that we are not mapping.

At this point a 'shelf' column and a 'box' column is created. This is specific for NHMD Vascular Plants which has shelves and boxes. 
- `Create column shelf based on column storagename using expression grel:if(value.split(' ')[0] == 'Shelf', value.split(' ')[1], '')`  
- `Create column box based on column storagename using expression grel:if(value.split(' ')[0] == 'Box', value.split(' ')[1], '')`


The following steps create the taxonomy based on the rank ID.  

- `Create column genus based on column taxonfullname using expression grel:if(cells['rankid'].value >= 180, value.split(' ')[0], '')`  
- `Create column species based on column taxonfullname using expression grel:if(cells['rankid'].value >= 220, value.split(' ')[1], '')`  
- `Create column subspecies based on column taxonfullname using expression grel:if(cells['rankid'].value == 230, value.split(' ')[2], '')`  
- `Create column variety based on column taxonfullname using expression grel:if(cells['rankid'].value == 240, value.split(' ')[3], '')`  
- `Create column forma at on column taxonfullname using expression grel:if(cells['rankid'].value == 260, value.split(' ')[3], '')`  


The time has come to add new[ *taxonRank* ] flags to the code.  
- Create column newgenusflag based on column genus using expression:
    - `grel:if((cells['newtaxonflag'].value=='True').and(cells['rankid'].value == 180), 'True', '')`  
- Create column newspeciesflag based on column taxonfullname using expression:
    - `grel:if((cells['newtaxonflag'].value=='True').and(cells['taxonfullname'].value.split(' ').length()==2), 'True',  '')`  
- Create column newsubspeciesflag based on column newtaxonflag using expression: 
    - `grel:if((cells['newtaxonflag'].value=='True').and(cells['taxonfullname'].value.split(' ').length()==3), 'True',  '')`  
- Create column newvarietyflag based on column newtaxonflag using expression:
    - `grel:if((cells['newtaxonflag'].value=='True').and(cells['taxonfullname'].value.contains(' var\\. ')), 'True',  '')`  
- Create column newformaflag based on column taxonfullname using expression: 
    - `grel:if((cells['newtaxonflag'].value=='True').and(cells['rankid'].value==260), 'True',  '')`


- Rename column familyname to family
- Rename column multispecimen to container  
- Rename column georegionname to broadgeographicalregion  


The broadgeographicalregion is duplicated into a column named 'localityname'.  
- Create column localityname based on column georegionname using expression grel:value  

The agentMiddleInitial must be checked to see if it has the value 'None'!

The column 'catalogeddate' is needed and must be created from a timestamp column 'recordeddatetime' which requires these steps:  
- "Create column catalogeddate based on column recorddatetime using expression grel:value.slice(0,10)"`  
- "Text transform on cells in column catalogeddate using expression value.toDate()"`  
- "Text transform on cells in column catalogeddate using expression grel:value.toString('dd/MM/yyyy')"`  

This time we catch any novel family names appearing:  
- Text transform on cells in column family using expression grel:if(cells['rankid'] < 180, '', value)  

Finally we need to add two columns for ready-to-publish and project-name:
- A novel column is made with the name 'publish' and the value 'True' signifying that the records are ready for publishing.
- Another column is needed: 'project' which contains the name 'DaSSCo'. This will make it easier to find records from the DaSSCo project.

#### Lastly reorder the column names to your liking

## Columns that can be removed:
#### (As the very last step)  

* ID
* spid
* taxonnameid
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