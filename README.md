# DaSSCo Mass Digitization App 

## Purpose of the application
The DaSSCo project is tasked with digitizing millions of specimens and to speed this process along, there needs to be a way to rapidly fill in data on 'storage', 'taxonomy', etc.  

![This is an image](https://github.com/NHMDenmark/DaSSCo/blob/main/docs/MADD_screencap.png)  

### Installation
Installation is done using a setup file that will ensure Python and all dependencies are put in place. The installer will also add a clean local database for registering entries in a "DaSSCo" folder under the user's documents folder. Be mindful to backup the database file upon reinstallation, so it is not overwritten and and data in it erased. 

Current release: 
(https://github.com/NHMDenmark/DaSSCo/releases/download/v0.1.0/DaSSCoSetup.v0.1.0.exe)

### Usage
There is a path to follow that requires only little training. A user must have credentials in order to employ the app. One could say that a specimen record is being created bit by bit and submitted to local DB at the end. 

#### Data entry  
After log in, the first section focuses on specimen storage location which has an autosuggest feature. The path leads through prep type and status, and into Geographic region and taxonomy. The latter also has the auto suggest feature. Auto-suggest takes three keystroke to query among all the names and returns a row object of names. As the input to which the keystrokes contribute increases, the smaller the subset gets at which point it is feasible to arrow down through the result until the desired name is reached and press _Enter_.  
The barcode is now ready for scanning. From there the record is ready to be 'saved'.  

#### Novel taxon names
Should a taxon name be inputted that is *not* contained in the taxonomic spine - a pop-up window appears in which the novel name can be inputted. There follows a similar event where the higher taxonomic name is asked for.  

### Data export  
As the app is designed to work "off line" all entries are stored locally. The entries thus registered can be exported to an Excel spreadsheet that can be imported into Specify. A smarter pipeline for getting the local data directly into Specify is currently being planned. 

### Licence and authorship
The application comes under the licence [licence] which aligns with the Open Source and Open Science frameworks. The [licence] was specifically selected because of [text by Pip> _ _ _ _ <end text].  
  
The authors of the application are :  
Fedor A. Steeman, NHMD  
Jan K. Legind, NHMD  

## For Developers 

### Structure
The app interfaces with a local SQLite database with tables for taxonomy (millions of names that are accessed according to the relevant discipline, say 'botany' for instance.) Storage while smaller also has its own table, as do Collection, Georegion and Institution. The table that is populated by the app is mainly 'specimen'.
Eventually, the local DB instances will be uploaded to a server where the data will be processed into Specify. The application also interfaces directly with Specify through the Specify7 API (more information further below). 

### Compilation  
For creating the executable, we used the Nuitka python compiler (https://nuitka.net/) using this command in the CLI:
```
python -m nuitka --windows-disable-console --follow-imports --onefile .\DaSSCo.py --plugin-enable=tk-inter
```  

Remember to activate venv and run pip install -r requirements.txt first

For creating the installer, we used Inno Setup and a definition file is located in the repo root as DaSSCO.iss

### Specify Interface 

In order to exchange information with Specify, the app has a module for interfacing with the Specify7 API. For now, this is mainly used for user authentication and basic info, but eventually this is planned to be built out into full synchronization in both directions. 
