# New data from the Mass Digitization App must be handled according to these guidelines

- The data files come into Exported_from_app_data_files directory
- Do a quick review of the data before proceeding to the post processing (OpenRefine stage). Use your favorite spreadsheet application but do not save the file as a spreadsheet.
- If the data is incomplete or has other issues contact the digitizer and write to Pip Brewer as well.
- If the data passes inspection then proceed to the post processing which currently takes place in OpenRefine. Details are here: https://github.com/NHMDenmark/Mass-Digitizer/blob/main/documentation/Postpreocessing_openRefine_documentation.md 
- When the post processing has been run. Check to see if the number of rows match what was expected. Check if all columns are there.
- Save the result as a TSV or CSV file in the Post_process_has_been_imported directory. Now might be a good time to have another set of eyes looking at the data.
- Now the data is ready for import into the live Specify portal through Workbench.
When you have done a successful import into Specify through Workbench, then there will be an existing 'upload plan' - please use this. It is a tremendous time saver and will prevent mistakes in mapping.
- Now it is time to save the workbench. Afterwards validate the project - there might be issues showing up at this point.
