CREATE EXTENSION if not exists plpython3u;
select * from pg_language;

SELECT * FROM pg_extension;

-- Определяемую пользователем скалярную функцию CLR,
-- определить в каком веке была создана картина
create or replace function century_of_creation(ida int)
returns int as $$
  plan = plpy.prepare("""select year_create
                      from artwork
                      where id_artwork = $1""", ["int"])
  year = plpy.execute(plan, [ida])
  if len(year) > 0:
    tmp = year[0]['year_create'] % 100
    if tmp > 0:
      return year[0]['year_create'] // 100 + 1
    else:
      return year[0]['year_create'] // 100
  else:
    return None
$$ language plpython3u;
select century_of_creation(0) as century;

select id_artwork, year_create from artwork;



-- Пользовательскую агрегатную функцию CLR,
create or replace function max_count_work_one_author()
returns int as $$
  result = plpy.execute("""
    select max(count_works) as max_work_one_author
    from (
      select id_author, count(*) as count_works
      from artwork
      group by id_author
    ) as tmp;
  """)
  if result and len(result) > 0:
    return result[0]['max_work_one_author']
  else:
    return none
$$ language plpython3u;
select max_count_work_one_author() as max_work_one_author;



-- Определяемую пользователем табличную функцию CLR, 
-- вывести id авторов чьи работы хранятся в базе и количество этих работ в порядке убывания
create or replace function authors_and_cnt_works()
returns table (id_author int, count_works int)
as $$
  result = plpy.execute("""
    select tmp.id_author, tmp.count_works
    from
      (select id_author, count(*) as count_works
      from artwork
      group by id_author) as tmp
    order by tmp.count_works desc""")
  return result if result else None;
$$ language plpython3u;
select *
from authors_and_cnt_works();

-- select tmp.id_author, tmp.count_works
-- from
-- 	(select id_author, count(*) as count_works
-- 	from artwork
-- 	group by id_author) as tmp
-- order by tmp.count_works desc


-- Хранимую процедуру CLR,
-- добавляет в таблицу history_exhibition случайные данные
create or replace procedure history_exhibition_adding()
as $$
  import random
  table_name = "history_exhibition"
  column_names = ', '.join(('id_artwork', 'id_exhibition'))

  # Получить результат
  len_history_exhibition = plpy.execute(f"SELECT count(*) as cnt from {table_name}")[0]['cnt']
  len_artwork = plpy.execute(f"SELECT count(*) as cnt from artwork")[0]['cnt']
  len_exhibition = plpy.execute(f"SELECT count(*) as cnt from exhibition")[0]['cnt']

  art_i = random.randint(0, len_artwork)
  exh_i = random.randint(0, len_exhibition)
  query = f"INSERT INTO {table_name} ({column_names}) VALUES ({art_i}, {exh_i});\n"
  plpy.execute(query)
$$ language plpython3u;

call history_exhibition_adding();

select count(*) from history_exhibition;

select * from history_exhibition
where id_artwork = 572;

-- • Триггер CLR,
create or replace function insert_into_history_exhibition()
returns trigger
as $$
  new = TD["new"]
  ia = new['id_artwork']
  ie = new['id_exhibition']
  plpy.notice(f"Произошла операция вставки в таблицу history_exhibition: ({ia}, {ie})")
$$ language plpython3u;

create or replace trigger trig_after_insert_history_exhibition
after insert on history_exhibition
for each row
execute function insert_into_history_exhibition();

drop trigger if exists trig_after_insert_history_exhibition on history_exhibition;



-- • Определяемый пользователем тип данных CLR. 
create type full_name as
(
  first_name text,
  last_name text
);

create or replace function get_full_name(id_author int)
returns full_name
as $$
  result = plpy.execute(f"select first_name, last_name from author where id_author = {id_author}")
  return result[0] if result else None
$$ language plpython3u;

select id_author, get_full_name(id_author) from author;