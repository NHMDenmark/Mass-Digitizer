CREATE VIRTUAL TABLE taxonname_fts USING fts5(id, name, fullname, rankid, treedefid, institutionid);