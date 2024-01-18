# Monitoring a directory 
We decided to monitor the "0.ForChecking" directory on Windows N drive for the sake of automating certain tasks. Automate was one of the keywords identified in the "DaSSCo Transcription Requirements workshop", so this effort could contribute nicely to speeding up the pipeline.  
The initial task is:
* To monitor the directory for new csv files coming in and renaming the file name by appending "_original" followed by the extension.
   
The current implementation relies on a Python solution:
https://github.com/NHMDenmark/DigitalCollections/tree/main/monitor_scripts 
This solution is hampered by the fact that it only works on a Windows machine. One of the reasons is that it relies on `win32file` and `win32con` libraries which are only available on the windows platform.  
The effort forms the base of future solutions involving automation as the Python environment makes it incredible flexible.



## History of the effort
This is largely  history of failed attempt to monitor a windows directory from different operating systems.  
Initially a MAC workstation was selected as the device performing the monitoring. At the onset, the monitor was tasked with identifying a new event and renaming csv files coming in according to a certain schema.
Both the MACOS Automator utility and the FSWatch turned out to be unsuitable for the monitoring task, since they did not pick up events on the windows system and were not able to rename the added files.  

Later a linux workstation became available and the effort was switched to the linux environment using bash scripting.  
The bash was based on the `inotifywait` utility and showed promise when tested on local drives. The script was based on this pattern:

inotifywait -m /path -e create -e moved_to |  
       &emsp; while read dir action file; do  
            &emsp;&emsp;&emsp;echo "The file '$file' appeared in directory '$dir' via '$action'"  
            &emsp;# do something with the file  
        &emsp;done  

The part "do something with the file" was replaced with a call to a python script.  
An attempt was made using the Watchdog library, but that was unable to read events from he N drive as well.
I believe the problem is the gap between operating systems : MACOS vs windows & Linux(Ubuntu) vs. windows. There is also different filesystems to consider.

## Future developments
I wish to implement the current code using the Watchdog library since it is a more elegant solution. The Event monitor will be its own class and the events will trigger methods in a module depending on the type of event. 
    
