
from sqlalchemy import func, select, exists
from tabs_classes import *
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import datetime

DB_SETTINGS = {
    "dbname": "postgres",
    "host": "localhost",
    "user": "postgres",
    "password": "163785303"
    # "port": 5432
}
engine = create_engine("postgresql://postgres:163785303@localhost/postgres")
session = Session(autoflush=False, bind=engine)

class Base(DeclarativeBase): pass

class Satellite(Base):
    __tablename__ = "satellite"
    __table_args__ = {"schema": "rk3"}

    id_satellite = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date_create = Column(Date)
    country = Column(String)

class Flight(Base):
    __tablename__ = "flight"
    __table_args__ = (
        PrimaryKeyConstraint('id_satellite', 'date_go', 'time_go'),
        {"schema": "rk3"}
    )
    id_satellite = Column(Integer)
    date_go = Column(Date)
    time_go = Column(String)
    week = Column(String)
    type = Column(Integer)

'''select *
from satellite
where country = 'россия'
order by date_create 
limit 1 '''
def oldest_setellite():
    print('Самый древний спутник в Росиии')
    q = session.query(Satellite).where(Satellite.country == 'Россия').order_by(Satellite.date_create)
    res = q.all()[0]
    print(f'RESULT: id={res.id_satellite}, name={res.name}')

oldest_setellite()


''' -- Спутник который в этом году первый вернулся на землю
select id_satellite, date_go, time_go
from rk3.flight
where type = 0 and date_part('year', date_go) = date_part('year', CURRENT_DATE)
ORDER BY time_go
LIMIT 1'''
def first_sattelite():
    print('Спутник который в этом году первый вернулся на землю')
    q = session.query(Flight).filter(
        Flight.type == 0,
        func.extract('year', Flight.date_go) == datetime.date.today().year).order_by(Flight.time_go)
    res = q.all()[0]
    print(f'RESULT: id={res.id_satellite}, date_go={res.date_go}, time_go={res.time_go}')

first_sattelite()


'''-- Все страны, в которых есть хотябы 1 космический аппарат, первый запуск которого был после 2024-10-01
select s.country
from rk3.satellite s
where EXISTS (
    select 1
    from rk3.flight f
    where s.id_satellite = f.id_satellite and 
        f.date_go > '2024-10-01' and f.type = 1
)'''
def get_counties():
    print('Все страны, в которых есть хотябы 1 космический аппарат, первый запуск которого был после 2024-10-01')
    q1 = (select(1).where(Flight.id_satellite == Satellite.id_satellite,
                            Flight.date_go > '2024-10-01',
                            Flight.type == 1))
    q = session.execute(select(Satellite.country).where(exists(q1)))
    print('RESULT: ', ', '.join(map(lambda x: x.country, q.all())))


get_counties()


