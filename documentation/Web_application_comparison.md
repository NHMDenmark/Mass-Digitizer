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
- In the table above NextPy has three questionmarks, because it is difficult to get sufficient information to be able to answer the question.

### Django
#### Advantages:
- A very mature framework that has been adopted by large companies (Discus, Spotify, Instagram ...)
- Has a reputation for excellent stability
- Has a large community and a wealth of 3rd party packages.

#### Disadvantages
- Complexity and steep learning curve. A term that regularly comes up is "clunky".
- Is likely to be costly in terms of development time.
- Monolithic which means that it might not lend itself well to micro-services type architecture. I would prefer a more modular approach.
- Django's ORM is largely geared towards SQL databases and less so towards NOSQL/Document databases.

### FastAPI
#### Advantages
- Performance bechmarks show FastAPI to have an advantage over other web frameworks.
- Has seen a meteoric rise and adoption which has created a large community.
- Tooled towards making API an easy effort and thereby facilitating modular code.

#### Disadvantages
- Fewer security features compared to Django.
- Due to it being a slimmer framework, it is not quite as comprehensive and its core functionalities are thus minimal.
