# Survey of NextPy, Django and FastAPI

Framework | NextPy | Django | FastAPI |
--- | --- | --- | --- |
Can run offline | ? | Can be done using Docker | Has a FastAPI-offline package |
Can be packaged into an .exe | ? | Problematic according to stackOverflow | Yes, but [1] |
Supports keyCloak | ? | Yes, also has built in auth. | Yes |
Integration with SQLite | Seems to be a work in progress [2] | Yes (SQLite > 3.27) | Yes |





[1] Might requires non trivial workarounds https://github.com/iancleary/pyinstaller-fastapi?tab=readme-ov-file & https://github.com/zauberzeug/nicegui/issues/691  

[2] https://github.com/dot-agent/nextpy/issues/125 


## Further comments

### NextPy: 
#### Advantages:
- Claims to be tooled towards Machine learning
- Is frontend and backend which ostencibly reduces complexity (Not sure this is actually an advantage)

#### Disadvantages
- A very young framework. First released in late 2023.
- Almost no documentation
- Nextpy.org website is offline and has been so for a while.
- 
