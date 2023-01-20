@echo off 
Rem Remember to install sqlite command tools first -> https://sqlite.org/download.html 
Rem Then add to PATH environment variables 

echo Preparing db edition... 

copy /y ..\..\db\db.sqlite3 ..\..\temp\db.sqlite3
echo Copied db base file to temporary folder 

cd ..\..\temp\
echo switched to temporary folder 

copy ..\sql\editions\NHMD\tracheophyta\NHMD-Tracheophyta-PrepTypes.sql Tracheophyta-PrepTypes.sql
sqlite3 db.sqlite3 ".read Tracheophyta-PrepTypes.sql"
del /f Tracheophyta-PrepTypes.sql
echo Added preparation types...

copy ..\sql\editions\NHMD\tracheophyta\NHMD-Tracheophyta-Highertaxa.sql Tracheophyta-Highertaxa.sql
sqlite3 db.sqlite3 ".read Tracheophyta-Highertaxa.sql"
del /f Tracheophyta-Highertaxa.sql
echo Added higher taxa...

copy ..\sql\editions\NHMD\tracheophyta\NHMD-Tracheophyta-Species-Batch1.sql Tracheophyta-Species-Batch1.sql
sqlite3 db.sqlite3 ".read Tracheophyta-Species-Batch1.sql"
del /f Tracheophyta-Species-Batch1.sql
echo Added species batch 1...

copy ..\sql\editions\NHMD\tracheophyta\NHMD-Tracheophyta-Species-Batch2.sql Tracheophyta-Species-Batch2.sql
sqlite3 db.sqlite3 ".read Tracheophyta-Species-Batch2.sql"
del /f Tracheophyta-Species-Batch2.sql
echo Added species batch 2...

copy ..\sql\editions\NHMD\tracheophyta\NHMD-Tracheophyta-Species-Batch3.sql Tracheophyta-Species-Batch3.sql
sqlite3 db.sqlite3 ".read Tracheophyta-Species-Batch3.sql"
del /f Tracheophyta-Species-Batch3.sql
echo Added species batch 3...

copy ..\sql\editions\NHMD\tracheophyta\NHMD-Tracheophyta-Species-Batch4.sql Tracheophyta-Species-Batch4.sql
sqlite3 db.sqlite3 ".read Tracheophyta-Species-Batch4.sql"
del /f Tracheophyta-Species-Batch4.sql
echo Added species batch 4...

copy ..\sql\editions\NHMD\tracheophyta\NHMD-Tracheophyta-Subspecies.sql Tracheophyta-Subspecies.sql
sqlite3 db.sqlite3 ".read Tracheophyta-Subspecies.sql"
del /f Tracheophyta-Subspecies.sql
echo Added subspecies...

copy ..\sql\editions\NHMD\tracheophyta\NHMD-Tracheophyta-VarForma.sql Tracheophyta-VarForma.sql
sqlite3 db.sqlite3 ".read Tracheophyta-VarForma.sql"
del /f Tracheophyta-VarForma.sql
echo Added infraspecific taxa other than subspecies...

xcopy ..\DaSSCo.dist\* DaSSCo.dist\*
copy /y ..\temp\db.sqlite3 temp\db.sqlite3
