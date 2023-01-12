# DaSSCo Mass Digitization App 

## Purpose of the application
The DaSSCo project is tasked with digitizing millions of specimens and to speed this process along, there needs to be a way to rapidly fill in data on 'storage', 'taxonomy', etc.  

![This is an image](https://github.com/NHMDenmark/Mass-Digitizer/blob/main/docs/appCAP.png?raw=true)  

### Installation
Installation is done using a setup file that will ensure all dependencies are in place. The installer will also add a clean local database for registering entries in a "DaSSCo" folder under the user's documents folder. Be mindful to backup the database file upon reinstallation, so it is not overwritten and and data in it erased. 

Downloads: 
(https://github.com/NHMDenmark/DaSSCo/releases/)

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
The application comes under the Apache-2.0 license which aligns with the Open Source and Open Science frameworks. 
  
The authors of the application are :  
Fedor A. Steeman, NHMD  
Jan K. Legind, NHMD  
Pip Brewer, NHMD

## Systems Architecture 

The app is written in python and consists of frontend components for easy user interfacing and backend component capable of both local storage and accessing external systems. The app is bundled with a local database file that is placed in a "DaSSCo" folder on the system it's installed on. In order to log on, and perform other functions, it needs to be connected to the internet. With the current state of the app, there are certain backend functions that have to be run by the developers in the development environment. 

More information on the Systems Architecture including a visual representation, see here: [Systems Architecture](https://github.com/NHMDenmark/Mass-Digitizer/blob/main/documentation/SystemsArchitecture.md)

## For Developers 

### Structure
The app interfaces with a local SQLite database with tables for taxonomy (millions of names that are accessed according to the relevant discipline, say 'botany' for instance.) Storage while smaller also has its own table, as do Collection, Georegion and Institution. The table that is populated by the app is mainly 'specimen'.
Eventually, the local DB instances will be uploaded to a server where the data will be processed into Specify. The application also interfaces directly with Specify through the Specify7 API (more information further below). 

### Compilation  
Begin with activating the virtual environment in console. [WINDOWS] CD to your project directory and `cd venv\Scripts\` and then type `.\activate`. This should switch the environment to venv. You can see the command line changes to `(venv) PS C:\Users\myUser\Documents`  
**Warning** If you get a security exception, you need to first start Powershell in admin mode and then put in :  
`Set-ExecutionPolicy Unrestricted -Force`  

For creating the executable, we used the Nuitka python compiler (https://nuitka.net/) using this command in the CLI:
```
python -m nuitka --windows-disable-console --follow-imports --onefile .\DaSSCo.py --plugin-enable=tk-inter --enable-plugin=numpy
```  

Remember to activate venv and run pip install -r requirements.txt first

For creating the installer, we use Inno Setup and a definition file for a generic edition is located in the repo root [DaSSCO.iss](https://github.com/NHMDenmark/Mass-Digitizer/DaSSCO.iss). The Inno Setup scripts bundles the database with the executable into an installer file. Before running the Inno Setup script, it is necessary to fill the database file with the taxonomic spine and other predefined data specific for the edition you would like to generate an installer for (see below).

#### Compiling App Editions 

Due to the size of the taxonomic spine, it is necessary to generate seperate editions for respective collections with differents of the database file that is bundled with the app. Under [MassDigitizer/editions](https://github.com/NHMDenmark/Mass-Digitizer/tree/main/MassDigitizer/editions/) there are folders for each edition containing a batch file that needs to be run in order to do so. The batch file will place the updated db.sqlite3 file in the [MassDigitizer/temp](https://github.com/NHMDenmark/Mass-Digitizer/tree/main/MassDigitizer/temp/) folder from where it will be picked up by Inno Setup. 

So the process for compilation are as follows: 
1. Create the executable using nuitka
2. Run the batch file to generate the db edition of choice 
3. Run the Inno Setup script to create the installer for this edition 
4. Repeat for the different editions giving each a distinct name

The different editions will be published alongside each other on the [Releases page](https://github.com/NHMDenmark/Mass-Digitizer/releases) 

### Specify Interface 

In order to exchange information with Specify, the app has a module for interfacing with the Specify7 API. For now, this is mainly used for user authentication and basic info, but eventually this is planned to be built out into full synchronization in both directions. 
