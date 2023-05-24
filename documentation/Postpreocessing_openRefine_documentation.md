# Steps in the refine tool post processing workflow
*Note -  I am using the term 'refine tool' to make the description  generic. The refine tool used was OpenRefine.


The digitiztion files come in Excel, TSV or CSV formats and have to be imported into the refine tool.

 Should there be numerical data columns that import as text formatted data, these need to be converted to numerical because there are GREL code that tests on the assumption that numbers are numbers.   
 - `"Text transform on cells in column taxonspid using expression value.toNumber()"`  
 - `"Text transform on cells in column rankid using expression value.toNumber()"`

A new column 'newtaxonflag' must be created. It will be important later on in the script. We derive this column from the 'taxonspid' field:  
- Create column newtaxonflag at index 11 based on column taxonspid using expression 
    - `grel:if((value==null).or(value==0), 'True', 'False')`
 

Next we need to split the 'storeagefullname' column by separator so that we can have the storage property in atomic units.  
- `"Split column storagefullname by separator"` The separator here is " | " (notice the leading and trailing whitespace)
- `"Rename column storagefullname 2 to site"`  
- `"Rename column storagefullname 3 to collection"` 
- `"Remove column storagefullname 1"` 

At this point we need a 'shelf' column and a 'box' column. This is specific for NHMD Vascular Plants which has shelves and boxes. 
- `Create column shelf based on column storagename using expression grel:if(value.split(' ')[0] == 'Shelf', value.split(' ')[1], '')` 
- `Create column box based on column storagename using expression grel:if(value.split(' ')[0] == 'Box', value.split(' ')[1], '')`


We have reached a place where taxonomy should be fleshed out.  

- `Create column genus based on column taxonfullname using expression grel:if(cells['rankid'].value >= 180, value.split(' ')[0], '')`  
- `Create column species based on column taxonfullname using expression grel:if(cells['rankid'].value == 220, value.split(' ')[1], '')`  
- `Create column subspecies based on column taxonfullname using expression grel:if(cells['rankid'].value == 230, value.split(' ')[2], '')`  
- `Create column variety based on column taxonfullname using expression grel:if(cells['rankid'].value == 240, value.split(' ')[3], '')`  
- `Create column forma at on column taxonfullname using expression grel:if(cells['rankid'].value == 260, value.split(' ')[3], '')`  

Another round must processed so that the taxonomic ranks can be populated:  
- Text transform on cells in column genus using expression:
    - `grel:if(cells['rankid'].value==180, cells['taxonfullname'].value.split(' ')[0], value)`  
- Text transform on cells in column species using expression:
    - `grel:if(cells['rankid'].value==220, cells['taxonfullname'].value.split(' ')[1], value)`  
- Text transform on cells in column subspecies using expression:
    - `grel:if(cells['rankid'].value==230, cells['taxonfullname'].value.split(' ')[2], value)`
- Text transform on cells in column variety using expression:   
    - `grel:if(cells['rankid'].value==240, cells[\"taxonfullname\"].value.split(' ')[3], value)`  
- Text transform on cells in column forma using expression:
    - `grel:if(cells['taxonfullname'].value==260, cells[\"taxonfullname\"].value.split(' ')[3], value)`

/abrogated
In order to pick out variety or forma taxa out of novel names we have to look at the name structure: Variety names will have `'var.'` in the name string. Likewise forma names will have the substring `' f.'`   
- `"grel:if(cells[\"taxonfullname\"].value.contains(\" f\\. \"), cells[\"taxonfullname\"].value.split(' ')[3], value)"`  
Variety:  
- `"grel:if(cells[\"taxonfullname\"].value.contains(\"var.\"), cells[\"taxonfullname\"].value.split(' ')[3], value)"`  

/end-abrogated

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
