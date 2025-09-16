@echo off
REM Remember to install sqlite command tools first -> https://sqlite.org/download.html
REM Then add to PATH environment variables

setlocal enabledelayedexpansion

cd temp\
echo Switched to temporary folder

echo Creating new skeleton database from script...
if exist db.sqlite3 (
    del /f db.sqlite3
    echo Old database deleted.
)

REM Create the database
echo Creating new database...
sqlite3 db.sqlite3 ".read ../../../db/create_db.sqlite3.sql"
if %errorlevel% neq 0 (
    echo Error: Failed to create database.
    exit /b 1
)
echo New database created.

REM Define editions and SQL files
set editions=NHMD\tracheophyta NHMD\entomology NHMA\entomology
set sqlfiles=PrepTypes TypeStatuses GeoRegions Storage Highertaxa Species-Batch1 Species-Batch2 Species-Batch3 Species-Batch4 Subspecies VarForma-Batch1 VarForma-Batch2 Hybrids

REM Process each edition and SQL file
for %%e in (%editions%) do (
    echo.
    echo ***** Preparing db edition %%e *****
    for %%s in (%sqlfiles%) do (
        echo Handling %%s
        if exist "..\%%e\%%s.sql" (
            copy "..\%%e\%%s.sql" "%%s.sql" >nul
            sqlite3 db.sqlite3 ".read %%s.sql"
            if !errorlevel! neq 0 (
                echo Error: Failed to execute %%s.sql
                exit /b !errorlevel!
            )
            del /f "%%s.sql"  REM Delete the copied SQL file
            echo Done.
        ) else (
            echo Warning: File ..\%%e\%%s.sql not found.
        )
    )
    echo ***********************************
)

REM Run optimizations
echo Running optimizations; One moment...
if exist "..\optimizations.sql" (
    copy "..\optimizations.sql" optimizations.sql >nul
    sqlite3 db.sqlite3 ".read optimizations.sql"
    if %errorlevel% neq 0 (
        echo Error: Failed to run optimizations.
        exit /b 1
    )
    del optimizations.sql
) else (
    echo Warning: optimizations.sql not found.
)

echo Done
exit /b 0