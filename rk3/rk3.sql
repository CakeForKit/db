create SCHEMA rk3;


CREATE TABLE IF NOT EXISTS rk3.satellite(
    id_satellite serial PRIMARY KEY,
    name text,
    date_create DATE,
    country text
);

CREATE TABLE IF NOT EXISTS rk3.flight(
    id_satellite INT,
    FOREIGN KEY (id_satellite) REFERENCES rk3.satellite(id_satellite),
    date_go DATE,
    time_go TIME,
    week text,
    type INT
);

insert into rk3.satellite (id_satellite, name, date_create, country)
VALUES (1, 'sit', '2050-01-01', 'Россия');

insert into rk3.satellite (id_satellite, name, date_create, country)
VALUES (3, 'sit', '2050-01-01', 'Россия');

insert into rk3.satellite (id_satellite, name, date_create, country)
VALUES (4, 'йцуйуй', '2050-01-01', 'Россия');

insert into rk3.satellite (id_satellite, name, date_create, country)
VALUES (5, 'ert', '2050-01-01', 'TTT');

insert into rk3.satellite (id_satellite, name, date_create, country)
VALUES (6, 'hyt', '2010-01-01', 'RRRR');

insert into rk3.satellite (id_satellite, name, date_create, country)
VALUES (2, 'шицян', '2049-12-01', 'Китай');

insert into rk3.flight (id_satellite, date_go, time_go, week, type)
VALUES (1, '2050-05-11', '9:00', 'Среда', 1);

insert into rk3.flight (id_satellite, date_go, time_go, week, type)
VALUES (5, '2050-05-11', '9:00', 'Среда', 1);

insert into rk3.flight (id_satellite, date_go, time_go, week, type)
VALUES (6, '2010-05-11', '9:00', 'Среда', 1);

insert into rk3.flight (id_satellite, date_go, time_go, week, type)
VALUES (1, '2051-06-14', '23:05', 'Среда', 0);

insert into rk3.flight (id_satellite, date_go, time_go, week, type)
VALUES (1, '2051-10-10', '23:50', 'Вторник', 1);

insert into rk3.flight (id_satellite, date_go, time_go, week, type)
VALUES (2, '2050-05-11', '15:15', 'Среда', 0);

insert into rk3.flight (id_satellite, date_go, time_go, week, type)
VALUES (1, '2052-01-01', '12:15', 'Понедельник', 0);

insert into rk3.flight (id_satellite, date_go, time_go, week, type)
VALUES (2, '2052-01-01', '9:0', 'Понедельник', 0);

insert into rk3.flight (id_satellite, date_go, time_go, week, type)
VALUES (1, '2050-01-01', '8:00', 'Понедельник', 0);

insert into rk3.flight (id_satellite, date_go, time_go, week, type)
VALUES (2, '2050-01-01', '18:00', 'Понедельник', 0);

insert into rk3.flight (id_satellite, date_go, time_go, week, type)
VALUES (1, '2024-11-01', '8:00', 'Понедельник', 0);

insert into rk3.flight (id_satellite, date_go, time_go, week, type)
VALUES (2, '2024-01-01', '18:00', 'Понедельник', 0);


-- ЗАДАНИЕ 1 ----START---

EXPLAIN ANALYSE

-- вывести топ 3 id_satellite отсортированные в порядке убывания по количеству полетов
select id_satellite
from rk3.flight
group by id_satellite
ORDER BY count(*) DESC
LIMIT 3


EXPLAIN ANALYSE
-- вывести пары спутников у которых страны одинаковые
select *
from rk3.satellite s1, rk3.satellite s2
where s1.country = s2.country and s1.id_satellite < s2.id_satellite

-- ЗАДАНИЕ 1 ----END---


-- ЗАДАНИЕ 2 ----START---
-- Самый древний спутник в Росиии
select *
from satellite
where country = 'Россия'
order by date_create 
limit 1


-- Спутник который в этом году первый вернулся на землю
select id_satellite, date_go, time_go
from rk3.flight
where type = 0 and date_part('year', date_go) = date_part('year', CURRENT_DATE)
ORDER BY time_go
LIMIT 1


-- Все страны, в которых есть хотябы 1 космический аппарат, первый запуск которого был после 2024-10-01
select s.country
from rk3.satellite s
where EXISTS (
    select 1
    from rk3.flight f
    where s.id_satellite = f.id_satellite and 
        f.date_go > '2024-10-01' and f.type = 1
)


-- ЗАДАНИЕ 2 ----END---

