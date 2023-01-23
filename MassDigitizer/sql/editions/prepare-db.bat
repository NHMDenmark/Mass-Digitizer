@echo off 
Rem Remember to install sqlite command tools first -> https://sqlite.org/download.html 
Rem Then add to PATH environment variables 
echo Preparing db edition
echo %1

IF [%1] == [] GOTO :NoParameter

copy %1\_test.txt _test.txt
if %errorlevel% NEQ 0 GOTO :InvalidPath

copy /y ..\..\db\db.sqlite3 ..\..\temp\db.sqlite3
echo Copied db base file to temporary folder 

cd ..\..\temp\
echo switched to temporary folder

set list=PrepTypes TypeStatuses GeoRegions Storage Highertaxa Species-Batch1 Species-Batch2 Species-Batch3 Species-Batch4 Subspecies VarForma
(for %%t in (%list%) do ( 
    echo Reading %%t
    copy ..\sql\editions\%1\%%t.sql %%t.sql
    sqlite3 db.sqlite3 ".read %%t.sql"
    echo Added %%t
    del /f %%t.sql
    echo *********************
))

cd ..\sql\editions
echo Exiting... 

exit /b 0 

:NoParameter
echo Please add parameter for edition path
exit /b 1

:InvalidPath
echo Please add a valid parameter for edition path
exit /b 1
