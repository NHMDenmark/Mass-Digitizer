# Import protocol

- The datasets from the DigiApp come into Exported_from_app_data_files directory (N drive)
- Path: `N:\SCI-SNM-DigitalCollections\DaSSCo\Digi App\Data\1.Exported files from App`
- After a file comes into this directory and the dataset is picked up by the data manager, it needs to be post processed according to `https://github.com/NHMDenmark/Mass-Digitizer/blob/main/documentation/Postprocessing_openRefine_documentation.md`. It is desirable to have the Exported_from_app_data_files directory almost empty which tells us the datasets that were exported are being post-processed and imported into Specify.
- Dataset is then moved to `N:\SCI-SNM-DigitalCollections\DaSSCo\Digi App\Data\2.PostProcessed_openRefine`
- Upload dataset to OpenRefine
- Map, save and validate in Workbench - then 'import'.  
- After the post processed dataset is imported into Specify it is moved into `N:\SCI-SNM-DigitalCollections\DaSSCo\Digi App\Data\3.Imported specify`.
   
OpenRefine steps: 
- Do a quick review of the data before proceeding to the post processing (OpenRefine provides a review on upload). 
- If the data is incomplete or has other issues contact the digitizer, and get in touch with Pip Brewer as well.
- If the data passes inspection then apply the post processing script: [Post processing script](https://github.com/NHMDenmark/Mass-Digitizer/blob/main/OpenRefine/post_processing.json)
- Documentation on the post processing script is located here: [Post processing documentation](https://github.com/NHMDenmark/Mass-Digitizer/blob/main/documentation/Postprocessing_openRefine_documentation.md)
- When the post processing has been run. Check to see if the number of rows match the number of inputted rows. Check if all columns are there. The Columns to be persisted are:
  - catalognumber
  - catalogeddate
  - notes
  - project
  - publish
  - container
  - family
  - genus
  - species
  - subspecies
  - variety
  - forma
  - newgenusflag
  - newspeciesflag
  - newsubspeciesflag
  - newvarietyflag
  - newformaflag
  - typestatusname
  - broadgeographicalregion
  - preptypename
  - site
  - collection
  - shelf
  - box
  - agentfirstname
  - agentmiddleinitial
  - agentlastname
  - recorddatetime  
- Make sure that the new column 'publish' which has the value "True" exists. This signifies that the records are to be published to GBIF. This is currently included in the GREL script.
- Check that the new column 'project' has been added which has the value "DaSSCo".
- It is imperative that taxonfullnames with qualifiers ('cf.', 'aff.', 'sp.') are handled, so that they won't automatically be interpreted as novel names. This means looking the Genus up in the taxonomy to determine if it is a known name or not. If known then determine the taxonspidID and add this manually.
- Save the result as a CSV file in the Post_process_NOT_been_imported directory.

Workbench steps
- Before embarking on he Workbench import, you must mention that an import is under way in the Specify chat.
- Log into the Specify7 site that corresponds to the institution that the data is generated at. 
- Switch to the relevant collection. 
- At this step the data is ready for import into Specify through Workbench.
- If an 'upload plan' exists, please use this.
- Now it is time to save the dataset. Afterwards validate the project - there might be issues showing up at this point.  
- A request must be sent to one of the Specify data coordinators (via the e-mail specify@snm.ku.dk) to have the specified range of dummy records deleted as well as the institution and collection. This means the new catalog numbers being used in the import must be sent to the above mentioned email. There are 250K reserved catalog numbers that must be freed for the new records to be accepted in Specify.
- After the reserved catalog numbers are removed the import can commence.
- Place the imported dataset in the `N:\SCI-SNM-DigitalCollections\DaSSCo\Digi App\Data\Imported` directory. This tracks already imported datasets.



