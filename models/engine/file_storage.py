#!/usr/bin/python3
"""Defines FileStorage class"""
import json
from models.Place import Place
from models.base_model import BaseModel
from models.City import City
from models.User import User
from models.Amenity import Amenity
from models.Review import Review
from models.State import State


class FileStorage:
    """Represent  abstracted storage engine """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        dname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(dname, obj.id)] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        oadict = FileStorage.__objects
        ojdict = {obj: oadict[obj].to_dict() for obj in oadict.keys()}
        with open(FileStorage.__file_path, "w") as j:
            json.dump(ojdict, j)

    def reload(self):
        """Deserialize JSON file __file_path to __objects"""
        try:
            with open(FileStorage.__file_path) as j:
                ojdict = json.load(j)
                for x in ojdict.values():
                    cls_name = x["__class__"]
                    del x["__class__"]
                    self.new(eval(cls_name)(**x))
        except FileNotFoundError:
            return
