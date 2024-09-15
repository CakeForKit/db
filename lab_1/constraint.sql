ALTER TABLE author 
ADD CONSTRAINT author_year_constraint CHECK (birth_year BETWEEN 0 AND 2024 AND
												death_year BETWEEN 0 AND 2024 AND
												birth_year < death_year);

ALTER TABLE artwork
ADD CONSTRAINT year_constraint CHECK (year_create BETWEEN 0 AND 2024);

ALTER TABLE owner_of_artworkship_history
ADD CONSTRAINT date_purchase_sale_constraint CHECK (date_purchase <= date_sale AND
                                                    date_sale <= NOW()::date);

ALTER TABLE exhibition
ADD CONSTRAINT date_exhibition_constraint CHECK (begin_date <= end_date);
