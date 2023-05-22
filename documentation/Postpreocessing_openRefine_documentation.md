# Steps in the refine tool post processing workflow
*Note -  I am using the term 'refine tool' to make the description  generic. The refine tool used was OpenRefine.


The digitiztion files come in Excel, TSV or CSV formats and have to be imported into the refine tool.

 Should there be numerical data columns that import as text formatted data, these need to be converted to numerical because there are GREL code that tests on the assumption that numbers are numbers.  
 `"description": "Text transform on cells in column catalognumber using expression value.toNumber()"`  
 `"description": "Text transform on cells in column taxonspid using expression value.toNumber()"`  
 `"description": "Text transform on cells in column rankid using expression value.toNumber()"`

A new column 'newtaxonflag' must be created. It will be important later on in the script. We derive this column from the 'taxonspid' field:  
`"description": "Create column newtaxonflag at index 11 based on column taxonspid using expression grel:if((value==null).or(value==0), 'True', 'False')"`
 

Next we need to split the 'storeagefullname' column by separator so that we can have the storage property in atomic units.  
`"description": "Split column storagefullname by separator"` The separator here is " | " (notice the leading and trailing whitespace)
`"description": "Rename column storagefullname 1 to institution"` ¤ Do we really want institution in there?  
`"description": "Rename column storagefullname 2 to site"`  
`"description": "Rename column storagefullname 3 to collection"`  

At this point we need a 'shelf' column and a 'box' column.  
`"description": "Create column shelf based on column storagename using expression grel:if(value.split(' ')[0] == 'Shelf', value.split(' ')[1], '')"`  
The box column is made in a similar way by replacing the word 'shelf' with 'box'.  
We have reached a place where taxonomy should be fleshed out.  

`"description": "Create column genus based on column taxonfullname using expression grel:if(cells['rankid'].value >= 180, value.split(' ')[0], '')"`  
`"description": "Create column species based on column taxonfullname using expression grel:if(cells['rankid'].value == 220, value.split(' ')[1], '')"`  
`"description": "Create column subspecies based on column taxonfullname using expression grel:if(cells['rankid'].value == 230, value.split(' ')[2], '')"`  
`"description": "Create column variety based on column taxonfullname using expression grel:if(cells['rankid'].value == 240, value.split(' ')[3], '')"`  
`"description": "Create column forma at on column taxonfullname using expression grel:if(cells['rankid'].value == 260, value.split(' ')[3], '')"`  

In order to pick out variety or forma taxa out of novel names we have to look at the name structure: Variety names will have `'var.'` in the name string. Likewise forma names will have the substring `' f.'`   
`"expression": "grel:if(cells[\"taxonfullname\"].value.contains(\" f\\. \"), cells[\"taxonfullname\"].value.split(' ')[3], value)"`  
Variety:  
`"expression": "grel:if(cells[\"taxonfullname\"].value.contains(\"var.\"), cells[\"taxonfullname\"].value.split(' ')[3], value)"`  

The time has come to add new[taxonRank]flags to the code.  
`"description": "Create column newformaflag based on column taxonfullname using expression grel:if((cells['newtaxonflag'].value=='True').and(cells['rankid'].value==260), 'True',  '')"`  
`"description": "Create column newvarietyflag based on column newtaxonflag using expression grel:if((cells['newtaxonflag'].value=='True').and(cells['taxonfullname'].value.contains(' var\\. ')), 'True',  '')"
  }`  
`"description": "Create column newsubspeciesflag based on column newtaxonflag using expression grel:if((cells['newtaxonflag'].value=='True').and(cells['taxonfullname'].value.split(' ').length()==3), 'True',  '')"`  
`"description": "Create column newspeciesflag at based on column taxonfullname using expression grel:if((cells['newtaxonflag'].value=='True').and(cells['taxonfullname'].value.split(' ').length()==2), 'True',  '')"
  }`  
`"description": "Create column newgenusflag based on column genus using expression grel:if((cells['newtaxonflag'].value=='True').and(cells['rankid'].value == 180), 'True', '')"`  
`"description": "Rename column familyname to family"`



- Create column name 'shelf' and 'box' from the 'storagename' column by 'Add column based on this column' 
  - the GREL script is `if(value.split(' ')[0] == 'Shelf', value.split(' ')[1], '')` - please exchange 'shelf' with 'box' for the second go-around.
- Create the 'genus' column based on 'taxonfullname' . The process is similar to above and the scrip is `if(cells['rankid'].value >= 180, value.split(' ')[0], '')`
- The same for 'species' and here the GREL is `if(cells['rankid'].value == 220, value.split(' ')[1], '')`  
- 


## Mapping
new[name]flag -> Determinations ->det.1 -> Taxon -> [rankname] -> Yes No1

## Columns that can be removed:
### As the very last step  

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
