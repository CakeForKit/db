-- vacuum full author, exhibition, history_exhibition, owner_of_artwork, owner_of_artworkship_history

-- -- 1. Инструкция SELECT, использующая предикат сравнения.
-- -- Список авторов 20 века
-- select * from author
-- 	where birth_year >= 1900 and death_year < 2000;

-- -- 2. Инструкция SELECT, использующая предикат BETWEEN
-- -- Получить список выставок начавшихся в жтом году
-- select * from exhibition
-- 	where begin_date between '2024-01-01' and now();

-- -- 3. Инструкция SELECT, использующая предикат LIKE. 
-- -- Получить произведения искусства, навзание которого состоит из 3х букв
-- select * from artwork
-- 	where name like '___'

-- -- 4. Инструкция SELECT, использующая предикат IN с вложенным подзапросом. 
-- -- Получить жанры произведений искусства кот были написаны творцами 20 века
-- select style 
-- 	from artwork
-- 	where id_author in (select id_author 
-- 						from author
-- 						where birth_year >= 1900 and death_year < 2000);

-- -- 5. Инструкция SELECT, использующая предикат EXISTS с вложенным подзапросом. 
-- -- Получить данные о людях которые владели каким либо произведением искусства больше 10 лет непрерывно
-- select ooa.id_owner_of_artwork, ooa.first_name, ooa.last_name,
-- 		history_of_ownership_artwork.date_purchase, history_of_ownership_artwork.date_sale
-- from (

-- 	select owner_of_artwork.id_owner_of_artwork, owner_of_artwork.first_name, owner_of_artwork.last_name
-- 		from owner_of_artwork
-- 		where exists (select 1
-- 						from history_of_ownership_artwork
-- 						where  (date_purchase + '10 years'::interval)::date <= date_sale)
						
-- ) as ooa 
-- join history_of_ownership_artwork
-- on ooa.id_owner_of_artwork = history_of_ownership_artwork.id_owner_of_artwork;


-- -- 6. Инструкция SELECT, использующая предикат сравнения с квантором.
-- -- Получить данные о произведениях искусства которые были созданы 
-- -- после года создания последней работы автора 8
-- select *
-- from artwork
-- where year_create >  ALL(select year_create
-- 							from artwork
-- 							where id_author = 8);

-- -- Вывести данные работах созданных автором 8 в порядке убывания годов создания
-- select *
-- from artwork
-- where id_author = 8
-- order by -year_create;



-- -- 7. Инструкция SELECT, использующая агрегатные функции в выражениях столбцов. 
-- -- Вывести id авторов чьи работы хранятся в базе и количество этих работ в порядке убывания
-- select tmp.id_author, tmp.count_works
-- from
-- 	(select id_author, count(*) as count_works
-- 	from artwork
-- 	group by id_author) as tmp
-- order by -tmp.count_works;


-- -- 8. Инструкция SELECT, использующая скалярные подзапросы в выражениях столбцов.
-- -- Получить максимальное количество работ принадлежащих одному автору
-- select max(tmp.count_works)
-- from
-- 	(select id_author, count(*) as count_works
-- 	from artwork
-- 	group by id_author) as tmp;

	
-- -- 9. Инструкция SELECT, использующая простое выражение CASE. 
-- -- 
-- select id_exhibition, title, begin_date,
-- 	case extract(year from begin_date)
-- 		when extract(year from now()) then 'This Year'
-- 		when extract(year from now()) - 1 then 'Last year'
-- 		else to_char(date_part('year', now()) - date_part('year', begin_date), '999D') || ' years ago'
-- 		end as m 
-- from exhibition;


-- -- 10. Инструкция SELECT, использующая поисковое выражение CASE.
-- -- 
-- select name, 
-- 	case
-- 		when year_create > 2000 then '21 век'
-- 		when year_create > 1900 then '20 век'
-- 		when year_create > 1800 then '19 век'
-- 		else '< 19 век'
-- 	end as century
-- from artwork

-- -- 11. Создание новой временной локальной таблицы из результирующего набора
-- -- данных инструкции SELECT. 
-- -- Вывести id авторов чьи работы хранятся в базе и количество этих работ в порядке убывания
-- select tmp.id_author, tmp.count_works
-- into TEMP
-- from
-- 	(select id_author, count(*) as count_works
-- 	from artwork
-- 	group by id_author) as tmp
-- order by -tmp.count_works;


-- 12. Инструкция SELECT, использующая вложенные коррелированные
-- подзапросы в качестве производных таблиц в предложении FROM. 
-- Коррелированным подзапросом называется подзапрос, который ссылается на значения столбцов внешнего запроса
-- Выставки проходившие в 2023 году и количество произведений икусства учавствовавших в них в порядке убывания этого количества

-- select ex.id_artwork, tmp.id_exhibition, tmp.title
-- from history_exhibition as ex
-- join (select id_exhibition, title
-- 		from exhibition
-- 		where title like 'a%')as tmp on ex.id_exhibition = tmp.id_exhibition
-- union (
-- select ex.id_artwork, tmp.id_exhibition, tmp.title
-- from history_exhibition as ex
-- join (select id_exhibition, title
-- 		from exhibition
-- 		where title like 'b%' and begin_date > '2000-01-01')as tmp on ex.id_exhibition = tmp.id_exhibition
-- );

-- select history_exhibition.id_artwork, count(*) as count_exh
-- from exhibition
-- 	join history_exhibition
-- 	on exhibition.id_exhibition = history_exhibition.id_exhibition
-- -- where begin_date >= '2010-01-01' and end_date < '2024-01-01'
-- group by history_exhibition.id_artwork
-- order by -count_exh;


-- select id_exhibition
-- from exhibition
-- 	where begin_date >= '2023-01-01' and end_date < '2024-01-01'


-- select tmp.id_author, tmp.count_works
-- into TEMP
-- from
-- 	(select id_author, count(*) as count_works
-- 	from artwork
-- 	group by id_author) as tmp
-- order by -tmp.count_works;



-- -- 13. Инструкция SELECT, использующая вложенные подзапросы с уровнем вложенности 3. 
-- -- получить данные о выставках с максимальный количеством работ
-- select *
-- from exhibition
-- where id_exhitition = 	(select id_exhitition
-- 						from history_exhibition
-- 						group by id_exhibition
-- 						having count(*) = 	(select max(count_artwork)
-- 											from   (select id_exhitition, count(*) as count_artwork
-- 													from history_exhibition
-- 													group by id_exhibition )
-- 											)
-- 						)



-- -- 14. Инструкция SELECT, консолидирующая данные с помощью предложения
-- -- GROUP BY, но без предложения HAVING.
-- -- Получить максимальное кол-во произведений скусства учавствовавших в выставке
-- select max(count_artwork)
-- from   (select id_exhitition, count(*) as count_artwork
-- 		from history_exhibition
-- 		group by id_exhibition )
-- )


-- -- 15. Инструкция SELECT, консолидирующая данные с помощью предложения
-- -- GROUP BY и предложения HAVING. 
-- -- получить данные о выставках с максимальный количеством работ
-- select id_exhibition, count(*) as count_artwork
-- from history_exhibition
-- group by id_exhibition
-- having count(*) = 	(select max(count_artwork)
-- 					from   (select id_exhibition, count(*) as count_artwork
-- 							from history_exhibition
-- 							group by id_exhibition )
-- 					)


-- select id_exhibition, count(*) as count_artwork
-- from history_exhibition
-- group by id_exhibition 
-- order by count_artwork desc;
-- select *
-- from history_exhibition;



-- -- 16. Однострочная инструкция INSERT, выполняющая вставку в таблицу одной
-- -- строки значений. 
-- insert into artwork (id_artwork, style, year_create, format, id_author)
-- values (1000, 'rococo0', 1744, 'painting', 25);

-- select * from author
-- where birth_year between 1580 and 1600

-- select * from artwork 
-- where id_artwork > 999


-- -- 17. Многострочная инструкция INSERT, выполняющая вставку в таблицу
-- -- результирующего набора данных вложенного подзапроса. 
-- insert into artwork (id_artwork, name, style, year_create, format, id_author)
-- values ((select count(*) from artwork), 
-- 		'siren', 'Baroque', 1610, 'pendant', 553)

-- -- 18. Простая инструкция UPDATE. 
-- update artwork
-- set name = 'Siren'
-- where name = 'siren'


-- -- 19. Инструкция UPDATE со скалярным подзапросом в предложении SET. 
-- update artwork
-- set name =	name || (select first_name
-- 					from author
-- 					where id_author = (select id_author 
-- 										from artwork
-- 										where id_artwork = 0))
-- where id_artwork = 0

-- select * 
-- from artwork 
-- join author 
-- on author.id_author = artwork.id_author
-- where id_artwork = 0


-- 20. Простая инструкция DELETE. 
-- insert into artwork (id_artwork, style, year_create, format, id_author)
-- values (9999, 'wer', 345, 'wefs', '0') 

-- select * from artwork
-- where id_artwork = 9999

-- delete from artwork
-- where id_artwork = 9999


-- 21. Инструкция DELETE с вложенным коррелированным подзапросом в
-- предложении WHERE. 
-- insert into exhibition (id_exhibition, title, begin_date, end_date, adress)
-- values (9999, 'tmp', '2024-10-10', '2024-10-11', 'qwerer');

-- insert into history_exhibition (id_artwork, id_exhibition)
-- values (0, 9999);

-- select * from history_exhibition where id_exhibition = 9999;
-- select * from exhibition where id_exhibition = 9999;

-- delete from history_exhibition
-- where id_exhibition in (select hiex.id_exhibition
-- 							from history_exhibition as hiex 
-- 							join exhibition as ex
-- 								on ex.id_exhibition = history_exhibition.id_exhibition
-- 							where ex.title = 'tmp')



-- -- 22. Инструкция SELECT, использующая простое обобщенное табличное
-- -- выражение
-- -- Обобщённые табличные выражения (CTE) — это один из видов запросов в системах управления базами данных.

-- получить данные о выставках с максимальный количеством работ
-- with exh_group as (
-- 	select id_exhibition, count(*) as count_artwork
-- 	from history_exhibition
-- 	group by id_exhibition
-- )
-- select *
-- from exh_group
-- where count_artwork = (	select max(count_artwork)
-- 						from exh_group
-- 						)


-- select id_exhibition, count(*) as count_artwork
-- 	from history_exhibition
-- 	group by id_exhibition
-- 	order by count_artwork desc


-- 23. Инструкция SELECT, использующая рекурсивное обобщенное табличное выражение.
-- select * from exhibition;
-- insert into exhibition (id_exhibition, title, begin_date, end_date, adress)
-- values (1000, 'tmp', '2024-10-10', '2024-10-11', 'qwerer');
-- insert into exhibition (id_exhibition, title, begin_date, end_date, adress)
-- values (1001, 'tmp', '2024-10-11', '2024-10-12', 'qwerer');
-- insert into exhibition (id_exhibition, title, begin_date, end_date, adress)
-- values (1002, 'tmp2', '2024-10-12', '2024-10-13', 'qwerer');

-- Получить подряд идущие дни
-- with RECURSIVE otv (ie, bd, ed) as
-- (
-- 	select id_exhibition, '2024-10-10'::date as beg, end_date
-- 	from exhibition
-- 	where begin_date = '2024-10-10'
-- 	union all
-- 	select ex.id_exhibition, ex.begin_date + 1, ex.end_date
-- 	from exhibition ex
-- 		join otv r 
-- 		on ex.begin_date = r.ed
-- )
-- select ie, bd, ed
-- from otv;


-- 24. Оконные функции. Использование конструкций MIN/MAX/COUNT OVER() 
-- select *,	max(id_artwork) over(partition by id_exhibition) as maxIdExibition,
-- 			min(id_artwork) over(partition by id_exhibition) as minIdExibition,
-- 			count(*) over(partition by id_exhibition) as countArts
-- from history_exhibition;


-- 25. Оконные фнкции для устранения дублей
-- Придумать запрос, в результате которого в данных появляются полные дубли.
-- Устранить дублирующиеся строки с использованием функции ROW_NUMBER()

-- -- Дублирование по title и adress (для полных дублей просто указать все атрибуты)
-- select * from (	select *, row_number() over(partition by title, adress) as r
-- 				from exhibition
-- ) where r > 1;

-- -- Вывести без дубликатов
-- select * from (	select *, row_number() over(partition by title, adress) as r
-- 				from exhibition
-- ) where r = 1;


-- order by id_exhibition desc;
