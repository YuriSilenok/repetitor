"""Состояния для изменения настроек"""
from aiogram.fsm.state import State, StatesGroup


class SettingsStates(StatesGroup):
    '''Состояния для настроек'''
    select_week = State()
    set_start_day = State()
    set_end_day = State()
