# Functional test procedure  

## Testing goals
To be written...

## Test scenarios

- Try to leave one field blank for every field in the App: Begin with 'Storage location' blank, then 'Prep. type', then 'Type status' etc.
- At all times try to provoke failure by skipping back and forth with [tab] and [alt-tab]
- All three collections need to be tested: NHMD Vascular plants, NHMD Entomology, NHMA Entomology.

☐ Log in with wrong credentials  
☐ Create three new entries  
☐ Go back to beginning  
☐ At every Go-back or -Forward step check to see if everything is carried over as expected. Does the database table content match what the APP displays?  
☐ Edit the first record  
☐ Edit the second record  
☐ Enter novel taxon name (name not existing in the app spine) - this addresses #305  
☐ Enter novel taxon name AND novel family name  
☐ Enter higher taxon name (level family or order)  
☐ Update the latest record  
☐ Set multi specimen checkbox  
☐ Try removing the multi specimen checkbox  
☐ Try removing the multi specimen tick mark from older records  
☐ Clear form - Update the latest record  
☐ Clear form – Create new record  
☐ Check that sticky fields are carried over to the new record: StorageFullname, PrepType, TypeStatus, Notes, MultiSpecimen, MultiSpecimen serial, GeoRegion, TaxonName  
☐ Create new record without green-area input  
☐ Create new record without Geo-region  
☐ Create new record with novel family name  
☐ Create new record with multispecimen ticked  
☐ Check to see if there is a meaningful error message when saving a record without a barcode  
- At every step of the way you need to check to see if the action resulted in an expected change in the database, so please have the DB editor open.

