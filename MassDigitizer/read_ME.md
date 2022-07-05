# SQLite as a fast read in-memory structure in Python

In order for the code `import_csv_memory.py` to work, there needs to be a taxonomy available in csv format.
Please unzip powo_uniq.zip or download this file: https://alumni-my.sharepoint.com/:x:/r/personal/btw897_ku_dk/Documents/DaSSCo/DaSSCo%20Workflows/Herbaria/powo_uniq.csv?d=w2e8c15c0533a408db59ba3fa716aa2e7&csf=1&web=1&e=bOXZrn  

The code will work with any taxonomy having the fields "taxon_name","family","authors","status".

The UI console will look like this:

![img](https://github.com/NHMDenmark/DaSSCo/blob/main/MassDigitizer/MADD_beta.png)

Once three or more characters have been put into the taxon name field, then the initial SQLite query is submitted. From thereon all operations are made on dictionaries.
The response size shrinks with every subsequent input until the result is less than 20, then a pop up window appears:
![pop](https://github.com/NHMDenmark/DaSSCo/blob/main/MassDigitizer/popup.png)  
  
## Process considerations
Several fast search options were considered to solve the issue of large taxonomies. I tested two of them: TypeSense and MeiliSearch and it was not a happy experience.
I ended up rejecting them because one returned data inconsistent with the ground truth dataset, and the other had issues with csv files though not with .json files. However the json file was three times larger than the corresponding csv file. I bumped into a 100MB limit soon enough.
Well known solutions such as ElasticSearch were not considered because the requirements stated that the app should work even if wifi was unavailable for a period of time. We ended up settling on using SQLite in memory as an adequate solution.  

## PS
Be aware that this code is still a work in progress.
