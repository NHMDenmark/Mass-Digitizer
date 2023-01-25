  -- To be run on Specify database 
  SELECT 	
	-- t.TaxonID taxonid, -- t.Name name, t.FullName fullname, t.RankID rankid, t.TaxonTreeDefID taxontreedefid, p1.FullName parentfullname, 
	CONCAT(
	-- 'INSERT INTO taxonname ("spid","name","fullname","rankid","taxontreedefid","parentfullname", "collectionid") VALUES (', 
	',(', t.TaxonID, ',"', t.Name, '","', t.FullName, '",', t.RankID, ',', t.TaxonTreeDefID, ',"', p1.FullName) -- 1 for NMHD, 2 for NHMA
	sqlstatement 
 FROM taxon t 
	JOIN taxon p1 ON p1.TaxonID = t.ParentID
	WHERE 
		t.taxontreedefid = 2 -- 13 for NHMD Botany, 5 for NHMD Entomology, 2 for NHMA Entomology 
		-- AND t.RankID = 200 -- ... 
		-- AND t.RankID = 230 -- Subspecies (NHMA: 240, NHMD: 230) 
		-- AND t.RankID = 240 -- Species (NHMA: 220, NHMD: 240) 
		AND t.RankID <= 180 -- Highertaxa (including Genus)  
		-- The following line is needed to restrict the taxa pulled out for NHMHD Entomology initially
		-- AND t.FullName IN ('Animalia', 'Arthropoda', 'Hexapoda', 'Insecta', 'Lepidoptera', 'Coleoptera', 'Aderidae','Agyrtidae','Alexiidae','Anthicidae','Anthribidae','Apionidae','Attelabidae','Biphyllidae','Bolboceratidae','Bostrichidae','Bothrideridae','Buprestidae','Byrrhidae','Byturidae','Cantharidae','Carabidae','Cerambycidae','Cerylonidae','Chrysomelidae','Ciidae','Clambidae','Cleridae','Coccinellidae','Corylophidae','Cryptophagidae','Cucujidae','Curculionidae','Dascillidae','Dasytidae','Dermestidae','Derodontidae','Drilidae','Dryopidae','Dytiscidae','Elateridae','Elmidae','Endomychidae','Erotylidae','Eucinetidae','Eucnemidae','Georissidae','Geotrupidae','Gyrinidae','Haliplidae','Helophoridae','Heteroceridae','Histeridae','Hydraenidae','Hydrochidae','Hydrophilidae','Hygrobiidae','Kateretidae','Laemophloeidae','Lampyridae','Latridiidae','Leiodidae','Limnichidae','Lucanidae','Lycidae','Lymexylidae','Malachiidae','Megalopodidae','Melandryidae','Meloidae','Microsporidae','Monotomidae','Mordellidae','Mycetophagidae','Nanophyidae','Nemonychidae','Nitidulidae','Nosodendridae','Noteridae','Oedemeridae','Orsodacnidae','Phalacridae','Phloeostichidae','Phloiophilidae','Prostomidae','Psephenidae','Ptiliidae','Ptinidae','Pyrochroidae','Pythidae','Rhynchitidae','Ripiphoridae','Salpingidae','Scarabaeidae','Scirtidae','Scraptiidae','Silphidae','Silvanidae','Spercheidae','Sphaeritidae','Sphindidae','Staphylinidae','Tenebrionidae','Tetratomidae','Throscidae','Trogidae','Trogossitidae','Zopheridae','Adelidae','Alucitidae','Argyresthiidae','Autostichidae','Batrachedridae','Bedelliidae','Blastobasidae','Bombycidae','Brahmaeidae','Bucculatricidae','Castniidae','Chimabachidae','Choreutidae','Coleophoridae','Cosmopterigidae','Cossidae','Crambidae','Depressariidae','Douglasiidae','Drepanidae','Elachistidae','Endromidae','Epermeniidae','Erebidae','Eriocraniidae','Ethmiidae','Euteliidae','Gelechiidae','Geometridae','Glyphipterigidae','Gracillariidae','Heliozelidae','Hepialidae','Hesperiidae','Incurvariidae','Lasiocampidae','Limacodidae','Lycaenidae','Lyonetiidae','Lypusidae','Micropterigidae','Momphidae','Nepticulidae','Noctuidae','Nolidae','Notodontidae','Nymphalidae','Oecophoridae','Opostegidae','Papilionidae','Parametriotidae','Peleopodidae','Pieridae','Plutellidae','Praydidae','Prodoxidae','Psychidae','Pterophoridae','Pyralidae','Riodinidae','Roeslerstammiidae','Saturniidae','Schreckensteiniidae','Scythrididae','Sesiidae','Sphingidae','Stathmopodidae','Tineidae','Tischeriidae','Tortricidae','Urodidae','Yponomeutidae','Ypsolophidae','Zygaenidae') 
		-- Lines to prevent duplicates caused by uploads 
		AND p1.FullName <> 'Uploaded'
		AND t.FullName <> 'Uploaded' 
	ORDER BY t.RankID -- For higher taxa
	-- ORDER BY t.fullName -- For species and below
LIMIT 250000 -- OFFSET 250000 -- increase the offset by 250000 until all taxa are retrieved