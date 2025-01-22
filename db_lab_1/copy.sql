-- DELETE FROM history_of_ownership_artwork;
-- DELETE FROM history_exhibition;
-- DELETE FROM artwork;
-- DELETE FROM author;
-- DELETE FROM owner_of_artwork;
-- DELETE FROM exhibition;

COPY author FROM '/var/lib/postgresql/data/pgdata/author.csv' delimiter ';' CSV;
COPY artwork FROM '/var/lib/postgresql/data/pgdata/artwork.csv' delimiter ';' CSV;
COPY owner_of_artwork FROM '/var/lib/postgresql/data/pgdata/owner_of_artwork.csv' delimiter ';' CSV;
COPY history_of_ownership_artwork FROM '/var/lib/postgresql/data/pgdata/history_of_ownership_artwork.csv' delimiter ';' CSV;
COPY exhibition FROM '/var/lib/postgresql/data/pgdata/exhibition.csv' delimiter ';' CSV;
COPY history_exhibition FROM '/var/lib/postgresql/data/pgdata/history_exhibition.csv' delimiter ';' CSV;


