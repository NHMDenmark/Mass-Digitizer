# Import protocol

- The datasets from the DigiApp come into Exported_from_app_data_files directory (N drive)
- The exports go initially into `N:\SCI-SNM-DigitalCollections\DaSSCo\Digi App\Data\0.For checking` so that Chelsea to check.
- If Chelsea needs to modify any of the spreadsheets, she saves them (so there is a copy) and changes "_original" to "_modified". She then moves the modified version or the original version if there have been no modifications to `N:\SCI-SNM-DigitalCollections\DaSSCo\Digi App\Data\1.Exported files from App` to be processed. 
- After a file comes into the `N:\SCI-SNM-DigitalCollections\DaSSCo\Digi App\Data\1.Exported files from App` directory and the dataset is picked up by the data manager, it needs to be post processed according to `https://github.com/NHMDenmark/Mass-Digitizer/blob/main/documentation/Postprocessing_openRefine_documentation.md`.
- Maker sure that the GREL script used in openRefine is the one which corresponds to the app release version used in the export.
- After a spreadsheet from `N:\SCI-SNM-DigitalCollections\DaSSCo\Digi App\Data\1.Exported files from App` has been processed in openRefine, a copy is saved and the "_original" suffix is changed to "_processed" on the copy. It can be moved to the next folder `N:\SCI-SNM-DigitalCollections\DaSSCo\Digi App\Data\2.PostProcessed_openRefine`. The original files can now be put in `N:\SCI-SNM-DigitalCollections\DaSSCo\Digi App\Data\4.Archive`
- Identify the catalog number range of the dataset and ask the Specify team to delete those records since they are reserved. Please mention which collection is to be deleted from. The account is: specify@snm.ku.dk
- Please mention that you are doing an import in the Specify chat in Slack.
- Map, save and validate in Workbench - then 'import'.  
- After the post processed dataset is imported into Specify it is moved into `N:\SCI-SNM-DigitalCollections\DaSSCo\Digi App\Data\3.Imported specify`.
- After the spreadsheets have been checked they should be moved to N:\SCI-SNM-DigitalCollections\DaSSCo\Digi App\Data\4.Archive
   
OpenRefine steps: 
- Do a quick review of the data before proceeding to the post processing (OpenRefine provides a review on upload). 
- If the data is incomplete or has other issues contact the digitizer, and get in touch with Pip Brewer as well.
- If the data passes inspection then apply the post processing script: [Post processing script](https://github.com/NHMDenmark/Mass-Digitizer/blob/main/OpenRefine/post_processing.json)
- Documentation on the post processing script is located here: [Post processing documentation](https://github.com/NHMDenmark/Mass-Digitizer/blob/main/documentation/Postprocessing_openRefine_documentation.md)
- When the post processing has been run. Check to see if the number of rows match the number of inputted rows. Check if all columns are there. The Columns to be persisted are:
  - project
  - catalognumber
  - newgenusflag
  - newspeciesflag
  - newsubspeciesflag
  - newvarietyflag
  - newformaflag
  - genus
  - species
  - subspecies
  - variety
  - newtaxonflag
  - forma
  - qualifier
  - taxonname
  - taxonnameid
  - family
  - taxonspid
  - highertaxonname
  - rankid
  - publish
  - taxonrankname
  - typestatusname
  - typestatusid
  - broadgeographicalregion
  - georegionid
  - localityname
  - storagefullname 1
  - site 
  - catalogeddate
  - collection
  - storagename
  - shelf
  - box
  - storagerankname
  - preptypename
  - notes
  - institutionname
  - collectionname
  - username
  - recorddatetime
  - agentfirstname
  - agentmiddleinitial
  - agentlastname
  - containertype
  - containername
     
(If more columns appear, it is no big deal since they will not be mapped in workbench)
- Make sure that the new column 'publish' which has the value "True" exists. This signifies that the records are to be published to GBIF. This is currently included in the GREL script.
- Check that the new column 'project' has been added which has the value "DaSSCo".
- It is imperative that taxonfullnames with qualifiers ('cf.', 'aff.', 'sp.') are handled, so that they won't automatically be interpreted as novel names. This means looking the Genus up in the taxonomy to determine if it is a known name or not. If known then determine the taxonspidID and add this manually.
- Please MAKE SURE that names of rank variety have ' var. ' before the specific epithet. The same with subvariety having ' subvar. '. Forma must have ' f. ' in that place and subforma the same with ' subf. '. Example: _Capsicum_ annuum var. glabriusculum
- In the 'Export drop down (top right) select "Custom tabular"
- Move to the 'Download' tab and change the Charcter encoding to 'windows-1252', then press the Download button
  The background for this is: Encoding disparity between post processing (openRefine) and Specify workbench. OpenRefine outputs utf-8 encoding by default while workbench expects win-1252 encoded input. This will corrupt many characters outside the ANSI range.
There is an update to Specify integrating utf-8 in the works. When it lands and when it will be operational for DaSSCo is pending information.
- The dataset records you are about to import into Specify have had their catalog numbers reserved for this task. Please identify the range of catalog numbers and submit this to specify@snm.ku.dk for deletion.

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




