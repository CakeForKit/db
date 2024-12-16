
--artwork_1999
select id_artwork
from artwork
where year_create > 1999

--sort_name
select name
from artwork
order by name

-- style_count
select style
from artwork
group by style
having count(*) > 3;


-- pair_style
select a1.id_artwork, a2.id_artwork, a1.style
from artwork a1
join artwork a2
on a1.style = a2.style and a1.id_artwork < a2.id_artwork


--artwork_and_author
select artwork.name, author.first_name, author.last_name 
from artwork 
join author 
on artwork.id_author = author.id_author



select *
from history_exhibition
where id_exhibition = 1


# воробушки - чтение с диска одной таблицы данных


explain ANALYSE
select * from artwork a
