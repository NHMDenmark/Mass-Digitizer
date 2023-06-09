# Import protocol

- The data files from the DigiApp come into Exported_from_app_data_files directory (N drive)
- Upload to OpenRefine 

OpenRefine steps: 
- Do a quick review of the data before proceeding to the post processing (OpenRefine stage). 
- If the data is incomplete or has other issues contact the digitizer, and get in touch with Pip Brewer as well.
- If the data passes inspection then apply the post processing script: [Post processing script](https://github.com/NHMDenmark/Mass-Digitizer/blob/main/OpenRefine/post_processing.json)
- Documentation on the post processing script is located here: [Post processing](https://github.com/NHMDenmark/Mass-Digitizer/blob/main/documentation/Postprocessing_openRefine_documentation.md)
- When the post processing has been run. Check to see if the number of rows match the number of inputted rows. Check if all columns are there as described in the documentation above.  
- Make sure that the new column 'Publish' which has the value "True" exists. This signifies that the records are to be published to GBIF. This is currently included in the GREL script.
- Make sure that the new column 'project' has been added which has the value "DaSSCo" exists
- Save the result as a CSV file in the Post_process_has_been_imported directory.

Workbench steps
- Log into the Specify7 site that corresponds to the institution that the data is generated at 
- Switch to the relevant collection 
- At this step the data is ready for import into Specify through Workbench.
- If an 'upload plan' exists, please use this.
- Now it is time to save the dataset. Afterwards validate the project - there might be issues showing up at this point.  
- A request must be sent to one of the Specify data coordinators (via the e-mail specify@snm.ku.dk) to have the specified range of dummy records deleted. This means the new catalog numbers being used in the import must be sent to the above mentioned email. There are 250K reserved catalog numbers that must be freed for the new records to be accepted in Specify.




