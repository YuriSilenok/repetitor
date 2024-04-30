'''База данных'''
from peewee import SqliteDatabase, Model, IntegerField, DateField, ForeignKeyField, TimeField, \
    CharField

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
    # короткие перерывы между занятиями
    rest_time = IntegerField(default=10)

class EventDuration(Table):
    """Продолжительности встречи"""
    user = ForeignKeyField(
        model=User,
        on_delete='CASCADE',
        on_update='CASCADE',
        backref='durations',
    )
    minutes = IntegerField(default=90)

class WeekDay(Table):
    """День недели"""
    name = CharField(unique=True)

class ScheduleTemplate(Table):
    """Хранит шаблон расписания рабочей недели"""
    user = ForeignKeyField(
        model=User,
        on_update='CASCADE',
        on_delete='CASCADE',
        backref='work_days',
    )
    week_day = ForeignKeyField(
        model=WeekDay,
        on_delete='CASCADE',
        on_update='CASCADE',
    )
    start_time = TimeField()
    end_time = TimeField()

class Lunch(Table):
    '''Перерыв на приём пищи'''
    start_time = TimeField()
    end_time = TimeField()
    schedule_template = ForeignKeyField(
        model=ScheduleTemplate,
        on_delete='CASCADE',
        on_update='CASCADE',
        backref='lunches'
    )

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
    week_day = ForeignKeyField(
        model=WeekDay,
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
    models=[User, EventDuration, WeekDay, ScheduleTemplate, Lunch, Event, Participant],
    safe=True,
)
days_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
for day in days_of_week:
    WeekDay.get_or_create(name=day)
db.close()
