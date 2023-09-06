# Changes and updates to the app code
- The app was rolled back to last stable version from July 6. due to issues with navigating back and forward. Many issues persisted despite the rollback.  
  For instance: The sorce code for the installer "App version 1.1.0" did not line up with the code going into the actual App inside the binary file.   
- Additional whitespace type characters in auto suggest taxonomic name are being stripped away #345
- Validation on the barcode/catalog number input was added checking length and type of the value according to the specific collection.
