# New data from the Mass Digitization App must be handled according to these guidelines

- The data files come into Exported_from_app_data_files directory
- Do a quick review of the data before proceeding to the post processing (OpenRefine stage). Use your favorite spreadsheet application but do not save the file as a spreadsheet for the purpose of OpenRefine.
- If the data is incomplete or has other issues contact the digitizer and write to Pip Brewer as well.
- If the data passes inspection then proceed to the post processing which currently takes place in OpenRefine. Details are here: https://github.com/NHMDenmark/Mass-Digitizer/blob/main/documentation/Postpreocessing_openRefine_documentation.md 
- When the post processing has been run. Check to see if the number of rows match what was expected. Check if all columns are there. Specifically we need to see if there are 'None' values being inserted which ought to be just empty cells. At the moment 'agentmiddleinitial' is set to 'None' for users having no middle initial. Please set these values to '' (empty string).  
- Be sure to add a new column 'Publish' which has the value "True". This is in order to track the records going into Specify.
- Save the result as a TSV or CSV file in the Post_process_has_been_imported directory. Now might be a good time to have another set of eyes looking at the data.
- At this step the data is ready for import into the live Specify portal through Workbench.
When you have done a successful import into Specify through Workbench, then there will be an existing 'upload plan' - please use this. It is a tremendous time saver and will prevent mistakes in mapping.
- Now it is time to save the workbench. Afterwards validate the project - there might be issues showing up at this point.  
- Before one start mapping into Workbench - _MAKE SURE_ you are on the correct server and collection/database: There is "specify-snm.science.ku.dk", "specify-test.science.ku.dk", and "specify-nhma.science.ku.dk" (NHMD, NHMD-test, Aarhus Herbarium), and in NHMD you have both Vascular Plants and Entomology. You have to access the right server AND the right collection.
- A request must be sent to one of the Specify data coordinators (via the e-mail specify@snm.ku.dk) to have the specified range of dummy records deleted. There are 250K reserved catalog numbers that must be freed for the new records to be accepted in Specify.
### Surprising issues solution


