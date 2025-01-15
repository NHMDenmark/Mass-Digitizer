# Post-processing of DaSSCo digitisation data via Species-Web

Post-processing is done via a Python script. As of right now, the script must be run manually but in the future it should be an automated process. 

The post-processing protocol can be found here: [Post-processing protocol](https://github.com/NHMDenmark/Mass-Digitizer/blob/main/documentation/postProcessing/import_protocol_postProcessing_speciesWeb.md)

The latest version of the Python script can be found here: [Format Data For Specify](https://github.com/NHMDenmark/Mass-Digitizer/blob/main/Species-Web/formatDataForSpecify.py)

Below you will find information on the steps performed by the Python script.

### Python script steps

1. The script locates any file ending with .csv in the specified folder
2. The data in the file is read into a dataframe for the script to work with
3. The filename is stored as a variable (called updated_filename) with either 'checked.csv' or 'checked_corrected.csv' replaced with 'processed.tsv'
4. Specified keys are extracted from the gbif_match_json column and assigned to their own columns: 

     - key
     - order
     - family
     - genus
     - species
     - scientificName
     - authorship
     - taxonomicStatus
     - acceptedKey
     - accepted

5. The key value dtype is assigned as Int64, with empty values being converted to null (This is both to prevent these values from being turned into floats and to prevent errors while working with this data later)
6. Several columns are added to the dataframe and filled with specified values:

     - datafile_remark = updated_filename
     - projectnumber = 'DaSSCo'
     - publish = 'True'
     - storedunder = 'True'
     - preptypename = 'Sheet'
     - count = '1'
     - datafile_source = 'DaSSCo data file'
     - cataloger_firstname = None
     - cataloger_middle = None
     - cataloger_lastname = None

7. The date in the date_asset_taken column is converted to datetime, extracted in the format YYYY-MM-DD, and added to both the catalogeddate column and the datafile_date column
8. The name (if any) in the digitiser column is converted to cataloger first, middle, and last name columns
9. The genus is split out of the species column and assigned to the genus column, as this data is more reliable than any value that may be in the genus field of the gbif_match_json results
10. Authorship values that do not contain any letters are converted to null values, in order to compensate for this field occasionally containing a comma or parentheses but no actual author name
11. The authorship, taxon key, and taxon key source are assigned to the appropriate rank level (genus, species, variety, or subspecies)
12. Taxon key fields are converted to int64 to prevent them from being turned into floats
13. If the taxon is a variety, everything in the scientificName column after 'var.' gets moved to a variety column
14. If the taxon is a subspecies, everything in the scientificName column after 'subsp.' gets moved to a subspecies column
15. If the species or subspecies values contain ' x ', it is assumed they are a hybrid and the value True gets assigned to the ishybrid column
16. The following columns are renamed:

     - barcode is renamed to catalognumber
     - area is renamed to broadgeographicalregion

17. A new column called locality is created and filled with the same value that is in broadgeographicalregion
18. If any rows contain the taxonomicStatus 'synonym', the following occurs:
    
     - These rows are assigned to a second dataframe called synonym_rows
     - Accepted columns are created at each rank level: 

         - accepted_genus 
         - accepted_species
         - accepted_variety
         - accepted_subspecies

     - The taxon string in the accepted column is parsed into the above relevant accepted columns
     - The author is pulled from the accepted column and added to the relevant accepted_author column at rank level
     - The accepted_taxon_key is assigned to the appropriate rank level (accepted_species_taxon_key, accepted_genus_taxon_key, etc)
     - The accepted_taxon_key_source at the relevant rank level is assigned the value 'GBIF'
     - If the accepted taxonomy is a hybrid, the accepted taxon field at the appropriate rank is filled with 'True' (either accepted_ishybrid_species or accepted_ishybrid_subspecies)
     - All taxonomy, author, key, and accepted columns that do not contain entirely null values are included and ordered in the final version of the synonym_rows dataframe
     - The synonym_rows dataframe is saved as a comma separated CSV file in the specified output_folder with the same name as the original CSV file, but 'synonymsToImport.csv' appended to the end in place of '_checked.csv', '_checked_corrected.csv'

19. The final order of all columns in the main dataframe is created and is as follows:

     - catalognumber
     - catalogeddate
     - cataloger_firstname
     - cataloger_middle
     - cataloger_lastname
     - projectnumber
     - publish
     - order
     - family
     - genus
     - genus author
     - genus_taxon_key 
     - genus_taxon_key_source
     - species 
     - species_author 
     - species_taxon_key 
     - species_taxon_key_source 
     - ishybrid_species
     - subspecies 
     - subspecies_author 
     - subspecies_taxon_key 
     - subspecies_taxon_key_source 
     - ishybrid_subspecies
     - variety 
     - variety_author 
     - variety_taxon_key 
     - variety_taxon_key_source 
     - storedunder
     - locality 
     - broadgeographicalregion 
     - preptypename 
     - count 

20. All above columns are confirmed to exist in the dataframe
21. All numeric columns are assigned the dtype int64 to prevent them from becoming floats
22. The dataframe is saved as a TSV file in the specified output_folder with the updated_filename
23. The original CSV file is moved to the specified archive_folder
24. The log_file is updated with the original filename, updated_filename, new locations, and a message that the TSV file is ready to be imported to Specify