## Initial tests
There are two database SQLite instances: One with index on the taxonname table, column fullname - and another without any indices on the taxonname table.
The dev machine specs are as follows:

OS Name: Microsoft Windows 10 Enterprise  
Version: 10.0.19044 Build 19044  
Other OS Description : Not Available  
OS Manufacturer: Microsoft Corporation  
System Name: SCI1018939  
System Manufacturer: LENOVO  
System Model: 11D2S16V00  
System Type: x64-based PC  
System SKU: LENOVO_MT_11D2_BU_Think_FM_ThinkCentre M90s  
Processor: Intel(R) Core(TM) i5-10500 CPU @ 3.10GHz, 3096 Mhz, 6 Core(s), 12 Logical Processor(s)  
Installed Physical Memory (RAM): 8,00 GB  
Total Physical Memory: 7,72 GB  
Available Physical Memory: 723 MB  
Total Virtual Memory: 12,5 GB  
Available Virtual Memory: 4,65 GB  
Page File Space: 4,75 GB  

I consider this an average workstation, not a speed demon.

The first test is using a simple SELECT query with two conditions:
`SELECT * FROM taxonname WHERE fullname LIKE lower("%car%") AND taxontreedefid = 13 AND rankid <=270  LIMIT 200;`

The table taxonname contains 1181252 records with nine columns.

The results are as follows:  
Table with indexed search column: 3 milliseconds (1 MS fetch)  
Table WITHOUT indexed search column: 13 milliseconds (4 MS fetch)  

Indexed search is faster than non-indexed search by a considerable margin.
Now searching with aggregate yields an even more pronounced difference.  
Here the query is such:  
`SELECT count(*), t.fullname FROM taxonname t GROUP BY 2;` (20,000 row fetch limit)  

All test are worst result of five queries.

Table with indexed search column: 34 milliseconds (27 MS fetch)  
Table WITHOUT indexed search column: 436 milliseconds (15 MS fetch)  

To give these results a bit of context; In competitive gaming a latency of 20MS is considered excellent. Sub 100MS is considered acceptable for gaming. Above 150MS is going to be noticeable and frustrating.  
I chose to look at the competitive gaming community because these users are very demanding of responsiveness and thus latency.

### Conclusion
Even with indexed tables I doubt the user can spot any difference. Nevertheless I added the index because it was an easy improvement to make.
