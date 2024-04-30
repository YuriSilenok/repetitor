'''База данных'''
from peewee import SqliteDatabase, Model, IntegerField, DateField, ForeignKeyField, TimeField

db = SqliteDatabase('db.db')

class Table(Model):
    '''что бы не указывать класс meta везде'''
    # pylint: disable=R0903
    class Meta:
        '''Все таблицы будут в одной БД'''
        database = db

class User(Table):
    '''Пользователь'''
    telegram_id = IntegerField()
    work_day_start_time = TimeField(
        formats='HH:MM',
        default='08:00'
    )
    work_day_end_time = TimeField(
        formats='HH:MM',
        default='19:30'
    )

class EventDuration(Table):
    """Продолжительности встречи"""
    user = ForeignKeyField(
        model=User,
        on_delete='CASCADE',
        on_update='CASCADE',
        backref='durations',
    )
    minutes = IntegerField(default=90)

class WorkDay(Table):
    """Рабочий день"""
    date = DateField()
    user = ForeignKeyField(
        model=User,
        on_update='CASCADE',
        on_delete='CASCADE',
        backref='work_days',
    )

class Event(Table):
    """Встреча или другое мероприятие"""
    start_time = TimeField()
    end_time = TimeField()
    owner = ForeignKeyField(
        model=User,
        on_update='CASCADE',
        on_delete='CASCADE',
        backref='events',
    )
    work_day = ForeignKeyField(
        model=WorkDay,
        on_update='CASCADE',
        on_delete='CASCADE',
        backref='events',
    )

class Participant(Table):
    """Участники встречи"""
    event = ForeignKeyField(
        model=Event,
        on_delete='CASCADE',
        on_update='CASCADE',
        backref='participants',
    )
    user = ForeignKeyField(
        model=User,
        on_delete='CASCADE',
        on_update='CASCADE',
        backref='participants'
    )

db.connect()
db.create_tables(
    models=[User, EventDuration, WorkDay, Event, Participant],
    safe=True,
)
db.close()
