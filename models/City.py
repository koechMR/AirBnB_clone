#!/usr/bin/python3
'''class inherent  BaseModel'''
from models.base_model import BaseModel


class City(BaseModel):
    '''class city'''

    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        """initializes City"""
        super().__init__(*args, **kwargs)
