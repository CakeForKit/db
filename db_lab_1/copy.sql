-- DELETE FROM history_of_ownership_artwork;
-- DELETE FROM history_exhibition;
-- DELETE FROM artwork;
-- DELETE FROM author;
-- DELETE FROM owner_of_artwork;
-- DELETE FROM exhibition;

COPY author FROM 'C:\data_db\author.csv' delimiter ';' CSV;
COPY artwork FROM 'C:\data_db\artwork.csv' delimiter ';' CSV;
COPY owner_of_artwork FROM 'C:\data_db\owner_of_artwork.csv' delimiter ';' CSV;
COPY history_of_ownership_artwork FROM 'C:\data_db\history_of_ownership_artwork.csv' delimiter ';' CSV;
COPY exhibition FROM 'C:\data_db\exhibition.csv' delimiter ';' CSV;
COPY history_exhibition FROM 'C:\data_db\history_exhibition.csv' delimiter ';' CSV;


