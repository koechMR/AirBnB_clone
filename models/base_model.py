#!/usr/bin/python3
"""Defines BaseModel class"""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Represents the BaseModel of the HBnB project."""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel.

        Args:
            *args (any): unused
            **kwargs (dict): key/value pairs of attributes
        """
        time_form = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for z, x in kwargs.items():
                if z == "created_at" or z == "updated_at":
                    self.__dict__[z] = datetime.strptime(x, time_form)
                else:
                    self.__dict__[z] = x
        else:
            models.storage.new(self)

    def to_dict(self):
        """Return dictionary of the BaseModel instance """
        readict = self.__dict__.copy()
        readict["created_at"] = self.created_at.isoformat()
        readict["updated_at"] = self.updated_at.isoformat()
        readict["__class__"] = self.__class__.__name__
        return readict

    def save(self):
        """Update updated_at with the current datetime"""
        self.updated_at = datetime.today()
        models.storage.save()

    def __str__(self):
        """Return  representation of the BaseModel instance"""
        vname = self.__class__.__name__
        return "[{}] ({}) {}".format(vname, self.id, self.__dict__)
