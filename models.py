'''База данных'''
from peewee import SqliteDatabase, Model, IntegerField, DateField, ForeignKeyField, TimeField, \
    CharField, BooleanField

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

class ScheduleTemplate(Table):
    """Хранит шаблон расписания рабочей недели"""
    user = ForeignKeyField(
        model=User,
        on_update='CASCADE',
        on_delete='CASCADE',
        backref='schedule',
    )
    week_day = CharField()
    work_start_time = TimeField(null=True)
    work_end_time = TimeField(null=True)
    lunch_start_time = TimeField(null=True)
    lunch_end_time = TimeField(null=True)
    timeout = IntegerField(null=True)
    enable = BooleanField(default=False)

class Event(Table):
    """Встреча или другое мероприятие"""
    date = DateField()
    start_time = TimeField()
    end_time = TimeField()
    owner = ForeignKeyField(
        model=User,
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
    models=[User, ScheduleTemplate, Event, Participant],
    safe=True,
)
db.close()
