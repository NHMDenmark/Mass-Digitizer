# Overall Systems Architecture

The Mass Digitization App is written in python and consists of frontend components for easy user interfacing and backend component capable of both local storage 
and accessing external systems. The app is bundled with a local database file that is placed in a "DaSSCo" folder on the system it's installed on. In order to 
log on, and perform other functions, it needs to be connected to the internet. 
With the current state of the app, there are certain backend functions that have to be run by the developers in the development environment. 

The user interface is based on the PySimpleGUI framework and as of the current version consists only of a login or "Home" window and a Specimen Data Entry window. 
These frontend components retrieve data through several backend components that, depending on the process and sort of data, either access the local app database 
or an external system via an API. 

## Program & Data flow

Whenever an end user starts the app, they will be presented with the home screen prompting them to log in using their Specify username and password 
and by choosing their respective institution and thereafter collection. 
Through the interface and API, the Specify software system is accessed to verify username/password and upon succesful login, the user is taken to the 
Specimen Data Entry form. 
The Specimen Data Entry form will pull predefined data from the local app database and also allow the end user to quickly add new specimen records to it. 

The app also has some code for merging taxon duplicates in Specify via the Specify interface and Specify7 API. 
In cases, where the author info is ambivalent between two taxon duplicates found, the GBIF interface is consulted for deciding the authorship. 
For now this code can only be run in the development environment by a Developer. 
The developer also has to run the Edition Script that prepares the local app database before compilation into an installer.
This is to fill the database with the taxonomic spine and other predefined data specific for the edition to be created. 
For the taxonomic spine, a snapshot of the current taxonomy is pulled from Specify database as SQL run by the edition script.  

<img width="1240" alt="MassDigitizationApp v0_2_6" src="https://user-images.githubusercontent.com/10909008/210967529-f7e75a32-1c72-4900-9fcd-b0647109ff29.png">

Not shown in this diagram is the process for exporting specimen data from the local app database in a format that then can be imported into Specify 
via the "Workbench" interface. 
