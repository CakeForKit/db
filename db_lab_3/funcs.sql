
-- СКАЛЯРНАЯ ФУНКЦИЯ
-- получить максимальное количество работ принадлежащих одному автору
create or replace function max_count_work_one_author()
returns int as $$
begin
	return (select max(tmp.count_works)
			from
				(select id_author, count(*) as count_works
				from artwork
				group by id_author) as tmp);
end;
$$ language plpgsql;
select max_count_work_one_author() as max_work_one_author;


-- ПОДСТАВЛЯЕМУЮ ТАБЛИЧНУЮ ФУНКЦИЮ
-- вывести id авторов чьи работы хранятся в базе и количество этих работ в порядке убывания
create or replace function authors_and_cnt_works()
returns table (id_author int, count_works int)
as $$
select tmp.id_author, tmp.count_works
from
	(select id_author, count(*) as count_works
	from artwork
	group by id_author) as tmp
order by tmp.count_works $$ 
language sql;
select *
from authors_and_cnt_works();


-- получить данные о выставках с максимальный количеством работ
with exh_group as (
	select id_exhibition, count(*) as count_artwork
	from history_exhibition
	group by id_exhibition
)
select *
from exh_group
where count_artwork = (	select max(count_artwork)
						from exh_group
						)

-- МНОГООПЕРАТОРНУЮ ТАБЛИЧНУЮ ФУНКЦИЮ
-- получить данные о выставках с максимальный количеством работ
create or replace function max_count_works()
returns table (id int, title varchar(100), count_artworks int) as $$ 
begin
    create temp table if not exists cnt_works (id_exh int, cnt int);

    insert into cnt_works 
        select id_exhibition, count(*) as cnt
        from history_exhibition
        group by id_exhibition;

    return query 
    select exh.id_exhibition, exh.title, cw.cnt
    from exhibition exh 
        join cnt_works cw 
        on exh.id_exhibition = cw.id_exh
    where cw.cnt = (select max(cnt)
                    from cnt_works);

    drop table if exists cnt_works;
end; 
$$ language plpgsql;
select id from max_count_works();

drop function if exists max_count_works;


-- РЕКУРСИВНУЮ ФУНКЦИЮ ИЛИ ФУНКЦИЮ С РЕКУРСИВНЫМ ОТВ
-- ряд фибоначи
create or replace function fact(cnt int, x int, x_ int)
returns table (res int) as $$
begin
	return query
	select x_;

	if cnt > 1 then
		return query
		select *
		from fact(cnt-1, x + x_, x);
	end if;
end;
$$ language plpgsql;
select *
from fact(40, 1, 0);

drop function if exists fact;


-- ХРАНИМУЮ ПРОЦЕДУРУ БЕЗ ПАРАМЕТРОВ ИЛИ С ПАРАМЕТРАМИ
-- продлить все выставки начавшиеся после st_date на plus_days дней
create or replace procedure extend_exhibitions(st_date date, plus_days int)
as $$
begin
    update exhibition
    set end_date = end_date + plus_days
    where begin_date >= st_date;
end;
$$ language plpgsql;

select * 
from exhibition
where begin_date >= '2024-09-01';

call extend_exhibitions('2024-09-01', 1);

drop Procedure public.extend_exhibitions(IN st_date date, IN plus_days integer);


-- РЕКУРСИВНУЮ ХРАНИМУЮ ПРОЦЕДУРУ ИЛИ ХРАНИМУЮ ПРОЦЕДУР С РЕКУРСИВНЫМ ОТВ
-- ряд фибоначи
create or replace procedure fact_proc(cnt int, x int, x_ int)
as $$
begin
	if cnt > 1 then
        raise notice '% = % + %', x + x_, x_, x;
		call fact_proc(cnt-1, x + x_, x);
    else 
        raise notice 'end';
	end if;
end;
$$ language plpgsql;
call fact_proc(10, 1, 0);

drop procedure if exists fact_proc;


-- хранимую процедуру с курсором
-- выводит дыты проведения выставок 
create or replace procedure all_dates()
as $$
declare
    be_date record;
    curs_date cursor for 
    select begin_date, end_date
    from exhibition
    order by begin_date;
begin
    open curs_date;
    loop
        fetch curs_date into be_date;
        exit when not found;
        raise notice '% -> %', be_date.begin_date, be_date.end_date;
    end loop;
    close curs_date;
end;
$$ language plpgsql;

call all_dates();


-- Хранимую процедуру доступа к метаданным
SELECT column_name, data_type, character_maximum_length, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'artwork';

create or replace procedure get_metadata(tab_name text)
as $$
declare
	data_ record;
	cur_table cursor for
		select c.column_name, c.data_type
		from information_schema.columns c
		where c.table_name = tab_name;
begin
	open cur_table;
	raise notice 'Table name = %', tab_name;
	loop
		fetch cur_table into data_;
		exit when not found;
		raise notice '%: %', data_.column_name, data_.data_type;
	end loop;
	close cur_table;
end;
$$ language plpgsql;

call get_metadata('artwork');


-- Триггер AFTER
create or replace function insert_into_authors()
returns trigger
as $$
begin 
	raise notice 'Произошла операция вставки в таблицу authors: %', new;
	return new;
end;
$$ language plpgsql;

create trigger trig_after_insert_authors
after insert on author
for each row
execute function insert_into_authors();

select * from author
order by id_author desc;

insert into author
values (1000, 'Карл', 'Брюллов', 1799, 1852);

delete from author
where id_author = 1000;

drop trigger if exists trig_after_insert_authors on author;



-- Триггер INSTEAD OF 
create or replace function stop_add_too_young_authors()
returns trigger
as $$
begin
    raise notice '----------------------------';
    if new.death_year - new.birth_year < 5 then
        raise exception 'ошибка вставки в tourists: возраст автора слишком мал';
		return null;
    else
        insert into author values (
            new.id_author, new.first_name, new.last_name, new.birth_year, new.death_year
        );
        raise notice 'вставка произошла успешно';
		return new;
    end if;
end;
$$ language plpgsql;

create or replace trigger stop_add_too_young_authors
instead of insert on author_view
for each row
execute function stop_add_too_young_authors();

drop view if exists author_view;
create view author_view as
select * from author;

insert into author_view
values (1001, 'Ваня', 'Иванов', 2022, 2024);

delete from author_view
where id_author = 1001;

select * from author_view
order by id_author desc;