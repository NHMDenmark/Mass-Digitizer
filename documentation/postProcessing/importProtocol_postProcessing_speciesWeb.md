# Import protocol: from Species-Web to Specify


### Overview

This import protocol consists of four steps:

1. Exporting the data from Species-Web
2. Checking the export files from Species-Web and resolving any issues
3. Post-processing via a Python script
4. Importing to Specify

The "Data" folder on the N-drive contains all the export files generated from the Digi App and has been structured with subfolders to accomodate the different steps of the protocol. Additional subfolders have been implemented for the separate institutions/collections involved in DaSSCo. Export files should always be placed in the appropriate subfolder according to the institution/collection that the digitised specimens belong to. Because of this existing file structure, Species-Web exports will initially be added to folders with names referencing the Digi App and OpenRefine, two tools which are not used in this workflow.

No automations are currently implemented as part of the import protocol. A folder has been added to the folder structure called "4.ReadyForScript". The plan is to have a monitoring script running on this directory in the future but currently the folder is not being used as part of the protocol.

### Exporting the data from Species-Web

As specimens are digitised, their data will be added to the Species-Web database (called 'dassco-au'). Once a week, this data will need to be exported from Species-Web and imported into Specify. In order to export the data from Species-Web, you'll need a terminal window and MySQL Workbench.

#### Protocol

1. Open the dassco-au database following the steps below:
   - Using powershell or another terminal, ssh into the species-web server
   - Open My SQL Workbench and connect to the dassco-au database
     - If this is your first time connecting to the database, open MySQL Workbench and click the plus sign next to MySQL Connections
     - A box will pop up that says Setup New Connection. Enter the following:
       - Connection Name: dassco-au
	     - Port: 3308
	     - Username: [enter your username]
	     - Password: [enter your password]
	     - Click OK
	   - The next time you open MySQL Workbench, you will see dassco-au under MySQL Connections

2. Run the SQL query located here: [Species-Web Export Query](https://github.com/NHMDenmark/Mass-Digitizer/blob/main/Species-Web/speciesWebExportQuery.sql), changing the date in this line: 

``WHERE folders.approved_at > '2025-01-01' LIMIT 100000``

3. Click the Export button and export the query results as a ; seperated CSV. Give the file a name matching the following format:

``AU_Herba_YYYYMMDD_HH_MM_INITIALS_original.csv``

where YYYYMMDD is the date of the export, HH is the hour of the export, MM is the minute of the export, and INITIALS is the exporter's initials

Save this file to 1.FromDigiApp/AU_Herbarium

### Checking the export files from Species-Web

Once the data has been exported, it will need to be checked over to make sure there are no obvious errors. A copy of the export will be made to ensure that the original data is not modified.

#### Protocol:

1.	Go to the 1.FromDigiApp/AU_Herbarium folder and locate the export
2.	Copy the file and paste it into the folder: 2.BeingChecked/AU_Herbarium
3.	To the end of the filename for the copied file, (the one in the 2.BeingChecked folder), append "_copy" so that the filename now ends with "_original_copy.csv"
4. Move the original file (the one without “copy” at the end) to the AU_Herbarium subfolder in the folder: 6.Archive
5.	Open the copied file using LibreOffice Calc and check for any errors or issues. Files with problems that require further investigation/time to resolve (e.g. files connected to github tickets) should be moved to the subfolder “FilesWithProblems” until the problem has been resolved
6.	When you are done checking the file, change the suffix of the filename from “original_copy” to “checked” (no corrections made) OR “checked_corrected”  (corrections/modifications have been made to the file)
7.	Move the file to the AU_Herbarium subfolder in the folder: 3.ReadyForOpenRefine


### Post-processing

Post-processing is done via a Python script, located here: [Format Data For Specify](https://github.com/NHMDenmark/Mass-Digitizer/blob/main/Species-Web/formatDataForSpecify.py).

Export files that are ready to be post-processed can be found in the folder: 3.ReadyForOpenRefine/AU_Herbarium, located in the Data folder on the N-drive. As part of the script, either one or two spreadsheets will be created to be imported to Specify, and the CSV file ending in either "_checked" or "_checked_corrected" will be moved to the 6.Archive/AU_Herbarium folder. 

A TSV file will always be created by the script. This is the formatted data that is ready for import to Specify. This file will retain the original filename, with "_checked.csv" or "_checked_corrected.csv" replaced by "_processed.tsv", and it will be saved in the folder: 5.ReadyForSpecify/AU_Herbarium.

If any organisms in the export have synonyms, a second CSV file will also be created with the associated taxonomic information of the synonyms. This file will also retain the original filename, with "_checked.csv" or "_checked_corrected.csv" replaced by "_synonymsToImport.csv" and it will be saved in the same folder as the TSV file.


#### Protocol:

1. Open a terminal window and navigate to where the script is stored
2. Run the script using the command `python formatDataForSpecify.py` 
3. The original CSV file (ending with _corrected.csv or checked_corrected.csv) is automatically moved to the 6.Archive/AU_Herbarium folder
4. The formatted TSV file is automatically moved to the 5.ReadyForSpecify/AU_Herbarium folder
5. If a synonyms file is created, this is also automatically moved to the 5.ReadyForSpecify/AU_Herbarium folder

### Import to Specify

Export files that are ready to be imported to Specify can be found in the "5.ReadyForSpecify" folder in the "Data" folder on the N-drive.

If a synonyms import file was created, this will need to be imported to Specify first so the synonymized taxa can be linked. Afterwards, the specimen records can also be imported.

#### Protocol (Importing Synonyms)

1. [Coming soon]

#### Protocol (Importing Specimen Records):

1. Log into the Specify7 site that corresponds to the institution that the data was generated at 
2. Choose the relevant collection 
3. Click on "Workbench" in the leftside menu
4. Click on "Import File", then choose the formatted TSV file from the last step
5. You will see a preview of the dataset. If the "Character encoding" is not set to "windows-1252", choose it from the dropdown menu 
6. Check that everything looks as expected. If it does, click "Save"
7. You need to define the mapping for the dataset. Click on "Create" and if you have imported DaSSCo export files before, click on "Choose Existing Plan" (if you do not have access to an existing plan, select "Collection Object" as a base table and find the mapping plan for the specific collection [here](https://github.com/NHMDenmark/Mass-Digitizer/tree/main/documentation/Specify_workbench_mapping))
8. Choose one of the previous imports to use the mapping plan from that import
9. Check the mapping to see if everything looks as expected. If it does, click "Save"
10. The data needs to go through a validation process before being imported. Click on "Validate" to validate the data
11. There might be errors showing up at this point (e.g. records that need to be disambiguated). If you correct any errors, you need to click "Save" and then run the validation again by clicking "Validate"
12. If there are no errors, click on "Import"
13. When the import is finished, click on "Results" to check the results of the import to see if everything looks as expected. You can also click "Create Record set" and then go through the individual records to do a more detailed quality check of the import
14. On the N-drive, move the file that was imported from one of the subfolders in “5.ReadyForSpecify” to the subfolder “MoveToArchive”
15. If you have additional files to import, move on to importing of the next file. Click on "Workbench" in the leftside menu and repeat steps 4-14
16. When finishing an importing session, on the N-drive move all the files from "MoveToArchive" to the appropriate subfolder in the "6.Archive" folder

