# DaSSCo Mass Digitization App 


## Purpose of app
The DaSSCo project is tasked with digitizing millions of specimens and to speed this process along, there needs to be a way to rapidly fill in data on 'storage', 'taxonomy', etc.  

![This is an image](https://github.com/NHMDenmark/DaSSCo/blob/main/docs/MADD_screencap.png)  

### Installation
The goal is to have the user download an executable file, so that each workstation won't need to have Python and all dependencies installed.  
Current release:  
(https://github.com/NHMDenmark/DaSSCo/releases/download/v0.1.0/DaSSCoSetup.v0.1.0.exe)
#### Installation instructions  
For creating this executable the Nuitka python compiler works fine (https://nuitka.net/). We used this command in the CLI:
```
python -m nuitka --windows-disable-console --follow-imports --onefile .\DaSSCo.py --plugin-enable=tk-inter
```  

Remember to activate venv and run pip install -r requirements.txt first

For Inno Setup use the definition file in the repo root called DaSSCO.iss : https://github.com/NHMDenmark/DaSSCo/blob/main/MassDigitizer/DaSSCo.iss
To put it briefly: Nuitka creates the exe file, while Inno-setup makes the setup file.

### Structure
The app interfaces with a local SQLite database with tables for taxonomy (millions of names that are accessed according to the relevant discipline, say 'botany' for instance.) 
Storage while smaller also has its own table, as do Collection, Georegion and Institution. The table that is populated by the app is mainly 'specimen'.
Eventually the local DB instances will be uploaded to a server where the data will be processed into Specify.  

### Usage
There is a path to follow that requires only little training. A user must have credentials in order to employ the app. One could say that a specimen record is being created bit by bit and submitted to local DB at the end. 
#### Data entry  
After log in, the first section focuses on specimen storage location which has an autosuggest feature. The path leads through prep type and status, and into Geographic region and taxonomy. The latter also has the auto suggest feature. Auto-suggest takes three keystroke to query among all the names and returns a row object of names. As the input to which the keystrokes contribute increases, the smaller the subset gets at which point it is feasible to arrow down through the result until the desired name is reached and press _Enter_.  
The barcode is now ready for scanning. From there the record is ready to be 'saved'.  
#### Novel taxon names
Should a taxon name be inputted that is *not* contained in the taxonomic spine - a pop-up window appears in which the novel name can be inputted. There follows a similar event where the higher taxonomic name is asked for.  

### Data export  
As the app is designed to work "off line" all entries are stored locally. Once the workstation comes online a call to the server is initiated and the database instance is uploaded for further processing.

