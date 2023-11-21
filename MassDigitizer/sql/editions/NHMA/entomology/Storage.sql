INSERT INTO storage (name, fullname, rankname, collectionid) VALUES 
("Lepidoptera DK (Pinned)","Natural History Museum Aarhus | Museum Storage (Universitetsparken) | Entomology Collections | Lepidoptera DK (Pinned)", "Collection", (SELECT id FROM collection WHERE spid = 32769 AND institutionid = 2)),
("Non-Lepidoptera DK (Pinned)","Natural History Museum Aarhus | Museum Storage (Universitetsparken) | Entomology Collections | Non-Lepidoptera DK (Pinned)", "Collection", (SELECT id FROM collection WHERE spid = 32769 AND institutionid = 2)),
("Transit Entomology (Pinned)","Natural History Museum Aarhus | Museum Storage (Universitetsparken) | Entomology Collections | Transit Entomology (Pinned)", "Collection", (SELECT id FROM collection WHERE spid = 32769 AND institutionid = 2))
;