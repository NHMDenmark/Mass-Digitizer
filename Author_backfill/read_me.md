# A spreadsheet utility to fill in author names for already registered specimens (via the Digi app).

Workflow on producing the spreadsheet:

Create a csv download from Specify UI. Mapping is as follows:

![Specify mapping](https://github.com/NHMDenmark/Mass-Digitizer/blob/main/Author_backfill/mappingSP.png)

Make sure that 'project' is set to 'DaSSCo' !

Import this csv as a table into the SQLite database that the Mass Digitization App made and name it 'binomial'. The code for the utility is specifically written for this scenario.
Create a new table 'binomial_id' by employing this SQL string:
CREATE TABLE binomial_id AS SELECT DISTINCT tw.genus, t.name, tw.box, tw.binomial, t.author, tw.taxonid FROM taxonauthor_storage_id tw JOIN taxonname t ON tw.binomial = t.name WHERE length(t.author) >= 1; 
Now the basic elements are in place.
