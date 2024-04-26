"""Состояния для изменения настроек"""
from aiogram.fsm.state import State, StatesGroup


class SettingsStates(StatesGroup):
    '''Состояния для настроек'''
    work_day_start_time = State()
    work_day_end_time = State()
    event_duration = State()
