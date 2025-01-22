-- "select category_name, count(*) as cnt from content " \
-- "join posts p on content.id = p.content_id " \
-- "group by category_name " \
-- "order by cnt desc;"


select id_author, count(*) as cnt
                        from artwork
                        group by id_author
                        order by cnt desc;



delete 
from posts 
where id = (select id 
            from posts 
            where title = 'test post' 
            order by date desc 
            limit 1) 
returning id;


select count(*) from artwork

select * 
from artwork
ORDER BY id_artwork desc

delete from artwork
where id_artwork = 1065

insert into artwork(id_artwork, name, style, year_create, format, id_author)
values (1000, 'aaa', 'ssss', '2000', 'd', '1')
returning id_artwork;


update artwork
set (id_artwork, name, style, year_create, format, id_author) = 
    (1000, 'ddd', 'rr', '3000', 'd', '2')
where id_artwork = 1000