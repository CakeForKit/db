
-- 1. из таблиц базы данных извлечь данные в json
copy (select row_to_json(t) from public.exhibition t) 
to 'c:\users\ck4te\archgit\db\db_lab_5\json_data\exhibition.json';

copy (select row_to_json(t) from public.owner_of_artwork t) 
to 'c:\users\ck4te\archgit\db\db_lab_5\json_data\owner_of_artwork.json';

copy (select row_to_json(t) from public.history_exhibition t) 
to 'c:\users\ck4te\archgit\db\db_lab_5\json_data\history_exhibition.json';

copy (select row_to_json(t) from public.author t) 
to 'c:\users\ck4te\archgit\db\db_lab_5\json_data\author.json';

copy (select row_to_json(t) from public.artwork t) 
to 'c:\users\ck4te\archgit\db\db_lab_5\json_data\artwork.json';

copy (select row_to_json(t) from public.history_of_ownership_artwork t) 
to 'c:\users\ck4te\archgit\db\db_lab_5\json_data\history_of_ownership_artwork.json';


select table_name
  from information_schema.tables
 where table_schema = 'public'
   and table_type = 'base table';



-- 2. выполнить загрузку и сохранение json файла в таблицу. 
-- созданная таблица после всех манипуляций должна соответствовать таблице
-- базы данных, созданной в первой лабораторной работ

drop table if exists public.author_new;
create table if not exists public.author_new(
    id_author serial not null,
    first_name varchar(100),
    last_name varchar(100),
    birth_year integer,
    death_year integer,
    primary key(id_author),
    constraint author_year_constraint check (((birth_year >= 0) and (birth_year <= 2024)) and ((death_year >= 0) and (death_year <= 2024)) and (birth_year < death_year))
);

drop table if exists public.author_json;
create table if not exists public.author_json
(
    data jsonb
);

COPY public.author_json(data) from 'C:\Users\ck4te\archgit\db\db_lab_5\json_data\author.json';

select * from public.author_json;

insert into public.author_new (id_author, first_name, last_name, birth_year, death_year)
select 
    (data->>'id_author')::INT,
    data->>'first_name',
    (data->>'last_name'),
    (data->>'birth_year')::INT,
    (data->>'death_year')::INT
from public.author_json;

select * from public.author_new;



-- 3. Создать таблицу, в которой будет атрибут(-ы) с типом JSON, или
-- добавить атрибут с типом JSON к уже существующей таблице. 
-- Заполнить атрибут правдоподобными данными с помощью команд INSERT или UPDATE.
  

create table if not exists public.tmp_arwork (
    id serial not null,
    name_art varchar(100),
    primary key(id),
    yg jsonb
);

insert into public.tmp_arwork (name_art, yg) 
values ('The Fighting Temeraire', '{"genre": "Impressionism", "year": 1839}'),
       ('Dance at Le Moulin de la Galette', '{"genre": "Impressionism", "year": 1876}'),
       ('Le Premier Disque', '{"genre": "Abstract", "year": 1912}');

select * from public.tmp_arwork;

update public.tmp_arwork
set yg = '{"genre": "Abstract art", "year": 1912}'
where id = 3;

select * from public.tmp_arwork;



-- 4. Выполнить следующие действия:
-- 4.1. Извлечь JSON фрагмент из JSON документа
select yg->>'genre' as genre,
       yg->>'year' as year
from public.tmp_arwork;


-- 2. Извлечь значения конкретных узлов или атрибутов JSON документа
select * 
from public.tmp_arwork
where yg->>'genre' = 'Impressionism'


-- 4. Изменить JSON документ
update public.tmp_arwork
set yg = jsonb_set(yg, '{cost}', '1000'::jsonb)
where id = 1;

-- 3. Выполнить проверку существования узла или атрибута
SELECT  id, name_art, 
    yg ? 'cost' as can_buy
from public.tmp_arwork;


-- 5. Разделить JSON документ на несколько строк по узлам

SELECT name_art,
    key, 
    value 
FROM 
    public.tmp_arwork, 
    jsonb_each_text(yg);
