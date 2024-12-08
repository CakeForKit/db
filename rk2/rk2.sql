
create schema rk;

create table rk.employees(
    id_employee serial primary key,
    name text,
    birth_year int,
    position text
);

alter table rk.employees 
add constraint employees_year_constraint check (birth_year between 0 and 2024);


-- виды валют
create table rk.types_currencies (
    id_tc serial primary key,
    currency text   -- название валюты
);

-- курсы валют
create table rk.rates (
    id_rates serial primary key,
    sale int,           -- продажа
    purchase int,        -- покупка
    id_tc int,
    unique(id_tc),
    foreign key (id_tc) references rk.types_currencies(id_tc)   -- валюта
);


-- операции обмена
create table rk.op_exchange (
    id_op serial primary key,
    id_employee int,    -- сотрудник
    foreign key (id_employee) references rk.employees(id_employee),
    id_rates int,          -- курсы валют
    foreign key (id_rates) references rk.rates(id_rates),
    sum_exchange int
);


-- простое выражение case
-- добавляет колонку m в которой указывается 
-- максимальная, минимальная или средняя по стоимости сумма операции
select id_employee, sum_exchange,
	case sum_exchange
        when (select max(sum_exchange) from rk.op_exchange) then 'Max'
        when (select min(sum_exchange) from rk.op_exchange) then 'Min'
        else 'middle'
        end as m 
from rk.op_exchange;


-- оконная функция
-- добавляет колонку max_sum_operation
-- которая показывает максимальную сумму операции для каждого сотрудника
select id_employee, sum_exchange,
    max(sum_exchange) over (partition by id_employee) as max_sum_operation
from rk.op_exchange;


-- консолидирующая данные с помощью предложения group by и having
-- получить информацию о сотрудниках которые проводили операции
-- больше чем с одной валютой
select id_employee, count(id_rates)
from rk.op_exchange
group by id_employee
having count(id_rates) > 1;


-- копирование таблицы по названию
CREATE OR REPLACE PROCEDURE rk.copy_table(original_table TEXT)
AS $$
DECLARE
    new_table TEXT;
    backup_date TEXT;
BEGIN
    backup_date := to_char(current_timestamp, 'YYYYDDMM');
    new_table := original_table || '_' || backup_date;
    IF EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'rk' 
          AND table_name = new_table
    ) THEN
        RAISE NOTICE 'Таблица % уже существует. Используется существующая таблица.', new_table;
    ELSE
        EXECUTE format('CREATE TABLE %I (LIKE %I INCLUDING ALL)', new_table, original_table);
        EXECUTE format('INSERT INTO %I SELECT * FROM %I', new_table, original_table);
        
        RAISE NOTICE 'Таблица % успешно скопирована в % .', original_table, new_table;
    END IF;
END;
$$ LANGUAGE plpgsql;

call rk.copy_table('employees');

select * from rk.employees_20241111;



