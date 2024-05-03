"""Состояния для изменения настроек"""
from aiogram.fsm.state import State, StatesGroup


class SettingsStates(StatesGroup):
    '''Состояния для настроек'''
    select_week = State()
    set_work_time_for_all = State()
    set_work_time = State()
    set_lunch_time_for_all = State()
    set_lunch_time = State()

    set_start_time_for_edit = State()
    set_end_time_for_edit = State()
