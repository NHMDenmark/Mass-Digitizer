INSERT INTO storage (name, fullname, collectionid) VALUES 
("Lepidoptera DK (Pinned)","Museum Storage (Universitetsparken) | Entomology Collections | Lepidoptera DK (Pinned)",(SELECT id FROM collection WHERE spid = 32769 AND institutionid = 2)),
("Non-Lepidoptera DK (Pinned)","Museum Storage (Universitetsparken) | Entomology Collections | Non-Lepidoptera DK (Pinned)",(SELECT id FROM collection WHERE spid = 32769 AND institutionid = 2)),
("Transit Entomology (Pinned)","Museum Storage (Universitetsparken) | Entomology Collections | Transit Entomology (Pinned)",(SELECT id FROM collection WHERE spid = 32769 AND institutionid = 2))
;