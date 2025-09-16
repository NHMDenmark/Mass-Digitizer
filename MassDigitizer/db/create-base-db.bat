@echo off
echo Creating new skeleton database from script...
if exist db.sqlite3 (
    del /f db.sqlite3
    echo Old database deleted.
)
sqlite3 db.sqlite3 ".read create_db.sqlite3.sql"
if %errorlevel% neq 0 (
    echo Error: Failed to create database.
    exit /b 1
)
echo New database created.
echo Done
exit /b 0