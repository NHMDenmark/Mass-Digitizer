# Monitoring a directory 
We decided to monitor the "0.ForChecking" directory on Windows N drive for the sake of automating certain tasks.
The current implementation relies on a Python solution:



## History of the effort
Initially a MAC workstation was selected as the device performing the monitoring. Initially the monitor was tasked with identifying a new event and renaming csv files coming in according to a certain schema.
Both the Automator utility and the FSWatch turned out to be unsuitable for the monitoring task, since they did not pick up events on the windows system and were not able to rename the added files.  

Later a linux workstation became available and the effort was switched to the linux environment using bash scripting.  
The bash was based on the `inotifywait` utility and showed promise when tested on local drives. The script was based on this pattern:

inotifywait -m /path -e create -e moved_to |  
       &emsp; while read dir action file; do  
            &emsp;&emsp;&emsp;echo "The file '$file' appeared in directory '$dir' via '$action'"  
            &emsp;# do something with the file  
        &emsp;done  

The part "do something with the file" was replaced with a call to a python script.  
I believe the problem is the gap between operating systems : MACOS vs windows & Linux(Ubuntu) vs. windows. There is also different filesystems to consider.

    
