from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship
from sqlalchemy import create_engine, Column, Integer, \
    String, ForeignKey, Date, CheckConstraint

DB_SETTINGS = {
    "dbname": "postgres",
    "host": "localhost",
    "user": "postgres",
    "password": "163785303"
    # "port": 5432
}

''' LINQ to Object. Создать не менее пять запросов с использованием всех
ключевых слов выражения запроса. Object - коллекция объектов, структура
которых полностью соответствует одной из таблиц БД, реализованной в
первой лабораторной работе '''


class Base(DeclarativeBase): pass


class Artwork(Base):
    __tablename__ = "artwork"

    id_artwork = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    style = Column(String)
    format = Column(String)
    id_author = Column(Integer, ForeignKey('author.id'))
    author_rel = relationship("Author", foreign_keys=[id_author])

class Author(Base):
    __tablename__ = "author"
    id_author = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_year = Column(Integer)
    death_year = Column(Integer)

class OwnerOfArtwork(Base):
    __tablename__ = "owner_of_artwork"
    id_owner_of_artwork = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    adress = Column(String)

class HistoryOfOwnershipArtwork(Base):
    __tablename__ = "history_of_ownership_artwork"
    id_owner_of_artwork = Column(Integer)
    id_artwork = Column(Integer)
    date_purchase = Column(Date)
    date_sale = Column(Date)

    ooa_rel = relationship("OwnerOfArtwork", foreign_keys=[id_owner_of_artwork])
    a_rel = relationship("Artwork", foreign_keys=[id_artwork])

class Exhibition(Base):
    __tablename__ = "exhibition"
    id_exhibition = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    begin_date = Column(Date)
    end_date = Column(Date)
    adress = Column(String)

class HistoryExhibition(Base):
    __tablename__ = "history_exhibition"
    id_exhibition = Column(Integer)
    id_artwork = Column(Integer)
    date_purchase = Column(Date)
    date_sale = Column(Date)

    e_rel = relationship("Exhibition", foreign_keys=[id_exhibition])
    a_rel = relationship("Artwork", foreign_keys=[id_artwork])


if __name__ == '__main__':
    engine = create_engine("postgresql://postgres:163785303@localhost/postgres")
    Session = sessionmaker(autoflush=False, bind=engine)
    with Session(autoflush=False, bind=engine) as db:
        art = db.query(Artwork).all()
        for p in art:
            print(f"{p.id_artwork}.{p.name} ({p.name})")