# Survey of NextPy, Django and FastAPI

Framework | NextPy | Django | FastAPI |
--- | --- | --- | --- |
Can run offline | ? | Can be done using Docker | Has a FastAPI-offline package |
Can be packaged into an .exe | ? | Problematic according to stackOverflow | Yes, but [1] |
Supports keyCloak | ? | Yes, also has built in auth. | Yes |
Integration with SQLite | Seems to be a work in progress [2] | Yes (SQLite > 3.27) | Yes |





[1] Might requires non trivial workarounds https://github.com/iancleary/pyinstaller-fastapi?tab=readme-ov-file & https://github.com/zauberzeug/nicegui/issues/691  

[2] https://github.com/dot-agent/nextpy/issues/125 
