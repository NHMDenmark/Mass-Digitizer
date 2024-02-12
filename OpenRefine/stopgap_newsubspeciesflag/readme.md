## Repo for temporary fixes for older Digi app exports 
This one deals with:
- new subspecies flag:
Here the remarks column is split by colon into two columns. Column 'remarks 2' is parsed for the substring "subsp." and the newsubspeciesflag is set to True. 
```
{
    "op": "core/text-transform",
    "engineConfig": {
      "facets": [
        {
          "type": "list",
          "name": "remarks",
          "expression": "value",
          "columnName": "remarks",
          "invert": false,
          "omitBlank": false,
          "omitError": false,
          "selection": [
            {
              "v": {
                "v": " | Verbatim_taxon:Galinsoga ciliata subsp. hispida",
                "l": " | Verbatim_taxon:Galinsoga ciliata subsp. hispida"
              }
            }
          ],
          "selectBlank": false,
          "selectError": false
        }
      ],
      "mode": "row-based"
    },
    "columnName": "newspeciesflag",
    "expression": "grel:if(cells['remarks 2'].value.length()=2, \"True\", \"\")",
    "onError": "keep-original",
    "repeat": false,
    "repeatCount": 10,
    "description": "Text transform on cells in column newspeciesflag using expression grel:if(cells['remarks 2'].value.length()=2, \"True\", \"\")"
  }
