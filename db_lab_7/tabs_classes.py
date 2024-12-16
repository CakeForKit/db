from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, \
    String, ForeignKey, Date, CheckConstraint, PrimaryKeyConstraint

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
    year_create = Column(Integer)
    id_author = Column('id_author', Integer, ForeignKey('author.id_author'))
    owners_rel = relationship("HistoryOfOwnershipArtwork")
    exhibitions_rel = relationship('HistoryExhibition')

class Author(Base):
    __tablename__ = "author"
    id_author = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_year = Column(Integer)
    death_year = Column(Integer)
    author_year_constraint = CheckConstraint('''birth_year BETWEEN 0 AND 2024 AND
												death_year BETWEEN 0 AND 2024 AND
												birth_year < death_year''')
    artwork_rel = relationship('Artwork')

class OwnerOfArtwork(Base):
    __tablename__ = "owner_of_artwork"
    id_owner_of_artwork = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    adress = Column(String)
    history_rel = relationship('HistoryOfOwnershipArtwork')

class HistoryOfOwnershipArtwork(Base):
    __tablename__ = "history_of_ownership_artwork"
    __table_args__ = (
        PrimaryKeyConstraint('id_owner_of_artwork', 'id_artwork'),
        {"schema": "public"}
    )
    id_owner_of_artwork = Column('id_owner_of_artwork', Integer, ForeignKey('owner_of_artwork.id_owner_of_artwork'))
    id_artwork = Column('id_artwork', Integer, ForeignKey('artwork.id_artwork'))
    date_purchase = Column(Date)
    date_sale = Column(Date)

class Exhibition(Base):
    __tablename__ = "exhibition"
    id_exhibition = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    begin_date = Column(Date)
    end_date = Column(Date)
    adress = Column(String)
    history_rel = relationship("HistoryExhibition")

class HistoryExhibition(Base):
    __tablename__ = "history_exhibition"
    __table_args__ = (
        PrimaryKeyConstraint('id_exhibition', 'id_artwork'),
        {"schema": "public"}
    )
    __mapper_args__ = {
        'confirm_deleted_rows': False
    }
    id_exhibition = Column('id_exhibition', Integer, ForeignKey('exhibition.id_exhibition'))
    id_artwork = Column('id_artwork', Integer, ForeignKey('artwork.id_artwork'))