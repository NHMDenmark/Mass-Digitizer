# Functional test procedure  

- Try to leave one field blank for every field in the App: Begin with 'Storage location' blank, then 'Prep. type', then 'Type status' etc.
- At all times try to provoke failure by skipping back and forth with [tab] and [alt-tab]
- All three collections need to be tested.

☐ Log in with wrong credentials  
☐ Create three new entries  
☐ Go back to beginning  
☐ Edit the first record  
☐ Edit the second record  
☐ Enter novel taxon name (name not existing in the app spine)  
☐ Enter novel taxon name AND novel family name  
☐ Update the latest record  
☐ Set multi specimen checkbox  
☐ Try removing the multi specimen checkbox  
☐ Try removing the multi specimen tick mark from older records  
☐ Clear all - Update the latest record  
☐ Clear all – Create new record  
☐ Create new record without green-area input  
☐ Create new record without Geo-region  
☐ Create new record without Taxonomy (should pop-up with error)  
☐ Create new record with novel family name  
☐ Create new record with multispecimen ticked  
☐ Then try creating another new record  
- At every step of the way you need to check to see if the action resulted in an expected change in the database, so please have the DB editor open.

