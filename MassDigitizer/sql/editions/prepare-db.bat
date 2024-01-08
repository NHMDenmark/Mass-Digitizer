@echo off 
Rem Remember to install sqlite command tools first -> https://sqlite.org/download.html 
Rem Then add to PATH environment variables 
Rem IF [%1] == [] GOTO :NoParameter

setlocal enabledelayedexpansion 
Rem for allowing ON ERROR GOTO

copy /y ..\..\db\db.sqlite3 temp\db.sqlite3
echo Copied db base file to temporary folder 
cd temp\
echo switched to temporary folder

set editions=NHMD\tracheophyta\ NHMD\entomology\ NHMA\entomology\
set sqlfiles=PrepTypes TypeStatuses GeoRegions Storage Highertaxa Species-Batch1 Species-Batch2 Species-Batch3 Species-Batch4 Subspecies VarForma-Batch1 VarForma-Batch2 Hybrids

(for %%e in (%editions%) do (
    echo
    echo ***** Preparing db edition %%e *****

    (for %%s in (%sqlfiles%) do ( 
        echo Handling %%s
        copy ..\%%e%%s.sql %%s.sql
        sqlite3 db.sqlite3 ".read %%s.sql"
        rem echo Added %%s
        del /f %%s.sql
        echo Done.
        rem echo **************************
        rem if !errorlevel! neq 0 exit /b !errorlevel!
    ))

    rem echo Done with %%e ... 
    echo ***********************************

))

echo Running optimizations; One moment...
copy ..\optimizations.sql optimizations.sql
sqlite3 db.sqlite3 ".read optimizations.sql"
del optimizations.sql
echo Done

exit /b 0 

:NoParameter
echo Please add parameter for edition path
exit /b 1

:InvalidPath
echo Please add a valid parameter for edition path
exit /b 1

