#!/usr/bin/python3
'''User class inherit from BaseModel'''
from models.base_model import BaseModel


class User(BaseModel):
    '''represent a class User'''

    email = ""
    password = ""
    first_name = ""
    last_name = ""
