INSERT INTO chronostratigraphy (spid, name, fullname, parentfullname, collectionid, treedefid, rankname, rankid) VALUES 
(0,"Unknown","Unknown","Unknown",(SELECT id FROM collection WHERE spid = 327682 AND institutionid = 1),1,"Stage",400),
(36,"Danian","Danian, Paleocene, Paleogene","Paleocene, Paleogene",(SELECT id FROM collection WHERE spid = 327682 AND institutionid = 1),1,"Stage",400),
(40,"Maastrichtian","Maastrichtian, Upper/Late, Cretaceous","Upper/Late, Cretaceous",(SELECT id FROM collection WHERE spid = 327682 AND institutionid = 1),1,"Stage",400)
;