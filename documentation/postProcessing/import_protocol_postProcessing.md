# Import protocol: from Digi App to Specify


### Overview

The import protocol consists of three steps:

1. Checking of the export files from the Digi App and resolving any issues
2. Post-processing in OpenRefine
3. Import to Specify

The "Data" folder on the N-drive contains all the export files  generated from the Digi App and has been structured with subfolders to accomodate the different steps of the protocol. Additional subfolders have been implemented for the separate institutions/collections involved in DaSSCo. Export files should always be placed in the appropriate subfolder according to the institution/collection that the digitised specimens belong to.

In the "6.Archive" folder within each institution/collection subfolder, further subfolders for each version of the Digi App have been implemented. Export files being moved to the "6.Archive" folder should always be placed in the appropriate subfolder according to the institution/collection that the digitised specimens belong to AND according to the version of the Digi App used at the time the specimens were digitised.

No automations are currently implemented as part of the import protocol. A folder has been added to the folder structure called "4.ReadyForScript". The plan is to have a monitoring script running on this directory in the future but currently the folder is not being used as part of the protocol.

### Checking of export files from DigiApp

Exported files from the DigiApp are saved to the N-drive in the appropriate subfolder in the “1.FromDigiApp” folder. 

As part of the new folder structure, subfolders have been implemented for the separate institutions/collections involved in DaSSCo. Files should always be placed in the appropriate subfolder according to the institution/collection that the digitised specimens belong to (will be clear from the filename).

#### Protocol:

1.	Go to the “1.FromDigiApp” folder, choose a subfolder, and choose a file to check (try to find the “next in line” file)
2.	Once you have decided on a specific file, make a copy of that file
3.	You now have two files, move the original file (the one without “copy” at the end) to the appropriate subfolder in the “6.Archive” folder (according to institution, collection, and version of the DigiApp)
4.	Move the copy you made to the appropriate subfolder in the “2.BeingChecked” folder
5.	Open the file and check for any errors or issues. Files with problems that require further investigation/time to resolve (e.g. files connected to github tickets) should be moved to the subfolder “FilesWithProblems” until the problem has been resolved
6.	When you are done checking the file, change the suffix of the filename from “original copy” to “checked” (no corrections made) OR “checked_corrected”  (corrections/modifications have been made to the file)
7.	Move the file to the appropriate subfolder in the “3.ReadyForOpenRefine” folder


### Post-processing

Post-processing is done in OpenRefine using a GREL script. The newest version of the GREL script can be found here:
[Post-processing script](https://github.com/NHMDenmark/Mass-Digitizer/blob/main/OpenRefine/post_processing.json)

Export files that are ready to be post-processed can be found in the "3.ReadyForOpenRefine" folder in the "Data" folder on the N-drive. There should be no need to check the data in detail before starting the post-processing since the export file should have been checked thoroughly before being moved to this folder.


#### Protocol:

1. Open OpenRefine
1. Click “Choose files” and choose a file in one of the subfolders in “3.ReadyForOpenRefine” on the N-drive (try to find the “next in line” file)
1. In the preview, the project name will be different from the filename since OpenRefine removes the underscores. Change the project name back to match the filename but change the suffix from "checked"/"checked_corrected" to “processed” 
1. Create the project
1. Move to the “Undo/Redo” tab on the left sidebar, click "Apply"
1. Copy and paste the entire post-processing script to the blank space and click “Perform Operations”
1. Move back to the “Facet/Filter” tab on the left sidebar
1. Find the “datafile_remark” column and open a Text facet for that column
1. Click on the project name and copy the name
1. In the Text facet box for "datafile_remark", choose “edit” for the value “insert filename”
1. Paste the project name in place of "insert filename" and add the extension “.tsv”
1. Do a quick check of the data to see if everything looks as expected
1. If everything looks good, go to “Export” and choose “Custom tabular exporter…”
1. Go to the “Download” tab and change “utf-8” to “windows-1252”. You can do this easily by clicking on the field and choosing “windows-1252” from the list
1. Click “Download”
1. Move the file from the "Downloads" folder on your computer to the appropriate subfolder in “5.ReadyForSpecify” on the N-drive
1. On the N-drive, move the file that was uploaded to OpenRefine from one of the subfolders in “3.ReadyForOpenRefine” to the subfolder “MoveToArchive”
1. Move on to post-processing of the next file. In OpenRefine, select "Open" from the top right menu and repeat steps 2-17
1. When finishing a post-processing session, on the N-drive move all the files from "MoveToArchive" to the appropriate subfolder in the "6.Archive" folder

### Import to Specify

Imports to Specify are performed using the Specify Workbench.

IMPORTANT! The dataset records you are about to import into Specify have had their catalog numbers reserved for this task. Please identify the range of catalog numbers in the export file and ask the Specify team to delete those reserved dummy records in Specify. Please also mention which institution and collection the dummy records should be deleted from. Submit this to specify@snm.ku.dk for deletion. When they have been deleted, move on to do the import.

ALSO! Before doing the import, please inform everyone in the "specify-specific" Slack channel that you are about to do an import in Specify. Please also let them know when you are done.

Export files that are ready to be imported to Specify can be found in the "5.ReadyForSpecify" folder in the "Data" folder on the N-drive.

#### Protocol:

1. Log into the Specify7 site that corresponds to the institution that the data was generated at 
1. Choose the relevant collection 
1. Click on "Workbench" in the leftside menu
1. Click on "Import File", then choose one of the files containing the reserved catalog numbers you had deleted from one of the subfolders in the "5.ReadyForSpecify" folder
1. You will see a preview of the dataset. If the "Character encoding" is not set to "windows-1252", choose it from the dropdown menu 
1. Check that everything looks as expected. If it does, click "Save"
1. You need to define the mapping for the dataset. Click on "Create" and if you have imported DaSSCo export files before, click on "Choose Existing Plan" (if you do not have access to an existing plan, select "Collection Object" as a base table and find the mapping plan for the specific collection [here](https://github.com/NHMDenmark/Mass-Digitizer/tree/main/documentation/Specify_workbench_mapping))
1. Choose one of the previous imports to use the mapping plan from that import
1. Check the mapping to see if everything looks as expected. If it does, click "Save"
1. The data needs to go through a validation process before being imported. Click on "Validate" to validate the data
1. There might be errors showing up at this point (e.g. records that need to be disambiguated). If you correct any errors, you need to click "Save" and then run the validation again by clicking "Validate"
1. If there are no errors, click on "Import"
1. When the import is finished, click on "Results" to check the results of the import to see if everything looks as expected. You can also click "Create Record set" and then go through the individual records to do a more detailed quality check of the import
1. On the N-drive, move the file that was imported from one of the subfolders in “5.ReadyForSpecify” to the subfolder “MoveToArchive”
1. Move on to importing of the next file. Click on "Workbench" in the leftside menu and repeat steps 4-14
1. When finishing an importing session, on the N-drive move all the files from "MoveToArchive" to the appropriate subfolder in the "6.Archive" folder

