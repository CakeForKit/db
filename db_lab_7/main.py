from tabs_classes import *
from sqlalchemy.orm import Session, aliased, class_mapper
from sqlalchemy import create_engine, func, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.exc import NoResultFound
from json import dumps, load

engine = create_engine("postgresql://postgres:163785303@localhost/postgres")
session = Session(autoflush=False, bind=engine)

'''LINQ to Object. Создать не менее пять запросов с использованием всех
ключевых слов выражения запроса. Object - коллекция объектов, структура
которых полностью соответствует одной из таблиц БД, реализованной в
первой лабораторной работе'''

# все произведения искусства которые били созданы после 1999
def artwork_1999():
    q = session.query(Artwork).where(Artwork.year_create > 1999)
    for r in q.all():
        print(r.id_artwork)
    print(str(q.statement.compile(dialect=postgresql.dialect())))

# artwork_1999()

# вывести названия произведения искусства в порядке возрастания
def sort_name():
    q = session.query(Artwork).order_by(Artwork.name)
    for r in q.all():
        print(r.id_artwork, r.name)
    print(str(q.statement.compile(dialect=postgresql.dialect())))

# sort_name()

# жанры искусства в которых больше 3х работ
def style_count():
    data = session.query(Artwork.style).group_by(Artwork.style).having(func.count('*') > 3).all()
    for r in data:
        print((r.style))

# style_count()

# вывести все пары произведений искусства у которых одинаковый жанр
def pair_style():
    a1 = aliased(Artwork)
    a2 = aliased(Artwork)
    q = session.query((a1.id_artwork).label("id_art1"),
                      (a2.id_artwork).label("id_art2"),
                      a1.style).\
        join(a2, a1.style == a2.style).filter(a1.id_artwork < a2.id_artwork)

    for r in q.all():
        print(r.id_art1, r.id_art2, r.style)
    print(str(q.statement.compile(dialect=postgresql.dialect())))

# pair_style()


'''LINQ to XML/JSON. Создать XML/JSON документ, извлекая его из таблиц
Вашей базы данных с помощью инструкции SELECT. Создать три запроса:
1. Чтение из XML/JSON документа.
2. Обновление XML/JSON документа.
3. Запись (Добавление) в XML/JSON документ.'''

def to_dict(model):
  columns = [c.key for c in class_mapper(model.__class__).columns]
  return dict((c, getattr(model, c)) for c in columns)

def artwork_to_json():
    serialized_labels = [
        to_dict(label)
        for label in session.query(Artwork).all()
    ]
    with open('artwork.json', 'w') as f:
        f.write(dumps(serialized_labels,indent=4))

# artwork_to_json()

def read_json():
    with open('artwork.json') as f:
        games = load(f)

    for g in games:
        print(g)

# read_json()

'''LINQ to SQL. Создать классы сущностей, которые моделируют таблицы
Вашей базы данных. Создать запросы четырех типов:
1. Однотабличный запрос на выборку.
2. Многотабличный запрос на выборку.
3. Три запроса на добавление, изменение и удаление данных в базе
данных.
4. Получение доступа к данным, выполняя только хранимую
процедуру.'''

# Однотабличный запрос на выборку.
# вывести информацию о датах выставок отсоритрованную по датам
def data_exhibition():
    q = session.query(Exhibition).order_by(Exhibition.begin_date)
    for r in q.all():
        print(r.begin_date, r.end_date)
    print(str(q.statement.compile(dialect=postgresql.dialect())))

# data_exhibition()


# Многотабличный запрос на выборку.
# Вывести информацию о произведении искусства и авторе
def artwork_and_author():
    q = session.query(Artwork.name, Author.first_name, Author.last_name).join(Author, Artwork.id_author == Author.id_author)
    for r in q.all():
        print(r.name, r.first_name, r.last_name)
    print(str(q.statement.compile(dialect=postgresql.dialect())))

# artwork_and_author()


def insert_history_exhibition(id_artwork, id_exhibition):
    he = HistoryExhibition()
    he.id_exhibition = id_exhibition
    he.id_artwork = id_artwork
    session.add(he)
    session.commit()

def update_history_exhibition(id_artwork, id_exhibition, new_id_exhibition):
    cnt = session.query(HistoryExhibition)\
        .filter(HistoryExhibition.id_exhibition == id_exhibition, HistoryExhibition.id_artwork == id_artwork)\
        .update({'id_artwork':new_id_exhibition})
    print('updated', cnt)
    session.commit()

def delete_history_exhibition(id_artwork, id_exhibition):
    try:
        elem = session.query(HistoryExhibition)\
            .filter(HistoryExhibition.id_exhibition == id_exhibition,
                    HistoryExhibition.id_artwork == id_artwork).one()
        session.delete(elem)
        session.commit()
    except NoResultFound:
        print('Элемента для удаления не найдено')

# insert_history_exhibition(100, 1)
# update_history_exhibition(100, 1, 333)
# delete_history_exhibition(333, 1)


def proc():
    session.execute(text(f"call extend_exhibitions('2024-09-01', 1);"))
    session.commit()

proc()
# if __name__ == '__main__':
#     engine = create_engine("postgresql://postgres:163785303@localhost/postgres")
#     Session = sessionmaker(autoflush=False, bind=engine)
#     with Session(autoflush=False, bind=engine) as db:
#         art = db.query(Artwork).all()
#         print(db.query(Artwork))
        # for p in art:
        #     print(f"{p.id_artwork}.{p.name} ({p.name})")