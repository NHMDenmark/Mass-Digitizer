# A spreadsheet utility to fill in author names for already registered specimens (via the Digi app).

Workflow for producing the spreadsheet author name backfill utility:

- Create a csv download from Specify UI. Mapping is as follows:

![Specify mapping](https://github.com/NHMDenmark/Mass-Digitizer/blob/main/Author_backfill/mappingSP.png)

  Make sure that 'project' is set to 'DaSSCo' !  
  This yields a dataset consiting of the taxonomy and the storage data. We will use this data in a JOIN statement later.

- Import this csv as a table into the SQLite database that the Mass Digitization App made and name it 'binomial'. The code for the utility is specifically written for this scenario.
Create a new table 'binomial_identifier' by employing this SQL string:

`CREATE TABLE binomial_identifier AS SELECT DISTINCT t.name, b.box,  t.author, t.dasscoid FROM binomial b JOIN taxonname t ON b.name = t.name WHERE length(t.author) > 0 ORDER BY 2;`   

Now the basic elements are in place.
