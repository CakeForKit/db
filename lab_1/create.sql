CREATE TABLE IF NOT EXISTS author(
id_author serial PRIMARY KEY,
first_name VARCHAR(100),
last_name VARCHAR(100),
birth_year INT,
death_year INT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS artwork(
id_artwork serial PRIMARY KEY,
style VARCHAR(100),
year_create INT,
format TEXT,
id_author INT DEFAULT NULL,
FOREIGN KEY (id_author) REFERENCES author(id_author) ON DELETE SET NULL
);

--CREATE TABLE IF NOT EXISTS author_artwork(
--id_author INT,
--id_artwork INT,
--FOREIGN KEY (id_author) REFERENCES author(id_author),
--FOREIGN KEY (id_artwork) REFERENCES artwork(id_artwork)
--);


CREATE TABLE IF NOT EXISTS owner_of_artwork(
id_owner_of_artwork serial PRIMARY KEY,
first_name VARCHAR(100),
last_name VARCHAR(100),
phone TEXT,
adress TEXT
);

CREATE TABLE IF NOT EXISTS owner_of_artworkship_history(
id_owner_of_artwork INT,
id_artwork INT,
FOREIGN KEY (id_owner_of_artwork) REFERENCES owner_of_artwork(id_owner_of_artwork),
FOREIGN KEY (id_artwork) REFERENCES artwork(id_artwork),
date_purchase DATE,
date_sale DATE
);

CREATE TABLE IF NOT EXISTS exhibition(
id_exhibition serial PRIMARY KEY,
title VARCHAR(100),
begin_date DATE,
end_date DATE,
adress VARCHAR(200)
);

CREATE TABLE IF NOT EXISTS history_exhibition(
id_artwork INT,
id_exhibition INT,
FOREIGN KEY (id_artwork) REFERENCES artwork(id_artwork),
FOREIGN KEY (id_exhibition) REFERENCES exhibition(id_exhibition)
);

