# Import protocol

- The data files come into Exported_from_app_data_files directory
- Upload to OpenRefine 

OpenRefine steps: 
- Do a quick review of the data before proceeding to the post processing (OpenRefine stage). Use your favorite spreadsheet application but do not save the file as a spreadsheet for the purpose of the OpenRefine step.
- Be careful that you do not open the exported data file in Excel because it tends to corrupt long integers. You can always make a copy of the file and then open it in MS Excel.
- If the data is incomplete or has other issues contact the digitizer, and get in touch with Pip Brewer as well.
- If the data passes inspection then proceed to the post processing which currently takes place in OpenRefine. Details are here: [post processing][https://pages.github.com/](https://github.com/NHMDenmark/Mass-Digitizer/blob/main/documentation/Postpreocessing_openRefine_documentation.md/)
- When the post processing has been run. Check to see if the number of rows match what was expected. Check if all columns are there (import list of columns desired).   
- Make sure that the new column 'Publish' which has the value "True" exists. This signifies that the records are to be published to GBIF. This is currently included in the GREL script.
- Make sure that the new column 'project' has been added which has the value "DaSSCo" exists
- Save the result as a TSV or CSV file in the Post_process_has_been_imported directory.

Workbench steps
- Log into the Specify7 site that corresponds to the institution that the data is generated at 
- Switch the collection 
- At this step the data is ready for import into Specify through Workbench.
When you have done a successful import into Specify through Workbench, then there will be an existing 'upload plan' - please use this. It is a tremendous time saver and will prevent mistakes in mapping.
- Now it is time to save the dataset. Afterwards validate the project - there might be issues showing up at this point.  
- A request must be sent to one of the Specify data coordinators (via the e-mail specify@snm.ku.dk) to have the specified range of dummy records deleted. This means the new catalog numbers being used in the import must be sent to the above mentioned email. There are 250K reserved catalog numbers that must be freed for the new records to be accepted in Specify.




