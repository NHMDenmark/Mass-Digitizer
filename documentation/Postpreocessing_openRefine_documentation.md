# Steps in the openRefine post processing workflow

- Import a file (Excel  or TSV) with the digitized export.
- If there are numerical (numbers, IDs etc.) columns which look formatted as text, then these need reformatting
  - Go to column and drop-down to 'Edit cells' then select 'Common transforms' and 'To number'
- A new column 'newtaxonflag' must be created. It will be important later on in the script.
  - Drop down on column 'taxonspid' and select 'Edit column' then 'Add column based on this column'
  - The GREL code is this: `if((value==null).or(value==0), 'True', 'False')`
- Next we need to split the 'storeagefullname' column by separator
  - Drop down 'storeagefullname' column and select 'Edit column' and 'Split into several columns'. The separator should be " | " (notice the leading and trailing whitespace)
- Rename the first to 'institution' (drop down -> Edit column -> Rename this column ). The second should be renamed 'site', and the third renamed 'collection'
- The last storage column is renamed 'storagename' 

- Create column name 'shelf' and 'box' from the 'storagename' column by 'Add column based on this column' 
  - the GREL script is `if(value.split(' ')[0] == 'Shelf', value.split(' ')[1], '')`
