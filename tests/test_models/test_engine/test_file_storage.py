#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py """
import os
import json
import unittest
import models
from datetime import datetime
from models.base_model import BaseModel
from models.Place import Place
from models.City import City
from models.User import User
from models.Amenity import Amenity
from models.State import State
from models.Review import Review
from models.engine.file_storage import FileStorage


class TestFileStorage_instantiation(unittest.TestCase):
    """Unittests for instantiation of the FileStorage class"""

    def test_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)

    def test_FileStorage_file_path_is_private_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def test_FileStorage_instantiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def testFileStorage_objects_is_private_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    
class TestFileStorage_methods(unittest.TestCase):
    """Unittests for methods of the FileStorage class"""
    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_new(self):
        Cy = City()
        Am = Amenity()
        Rv = Review()
        Bm = BaseModel()
        Pl = Place()
        Us = User()
        St = State()
        models.storage.new(Pl)
        models.storage.new(Cy)
        models.storage.new(Bm) 
        models.storage.new(St)
        models.storage.new(Am)
        models.storage.new(Rv)
        models.storage.new(Us)
        self.assertIn("Amenity." + Am.id, models.storage.all().keys())
        self.assertIn(Am, models.storage.all().values())
        self.assertIn("Review." + Rv.id, models.storage.all().keys())
        self.assertIn(Rv, models.storage.all().values())
        self.assertIn("BaseModel." + Bm.id, models.storage.all().keys())
        self.assertIn(Bm, models.storage.all().values())
        self.assertIn("User." + Us.id, models.storage.all().keys())
        self.assertIn(Us, models.storage.all().values())
        self.assertIn("State." + St.id, models.storage.all().keys())
        self.assertIn(Pl, models.storage.all().values())
        self.assertIn("City." + Cy.id, models.storage.all().keys())
        self.assertIn(Cy, models.storage.all().values())
        self.assertIn(St, models.storage.all().values())
        self.assertIn("Place." + Pl.id, models.storage.all().keys())
        

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        Bm = BaseModel()
        Us = User()
        St = State()
        Pl = Place()
        Cy = City()
        Am = Amenity()
        Rv = Review()
        models.storage.new(Bm)
        models.storage.new(Us)
        models.storage.new(St)
        models.storage.new(Pl)
        models.storage.new(Cy)
        models.storage.new(Am)
        models.storage.new(Rv)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as x:
            save_text = x.read()
            self.assertIn("BaseModel." + Bm.id, save_text)
            self.assertIn("Place." + Pl.id, save_text)
            self.assertIn("City." + Cy.id, save_text)
            self.assertIn("User." + Us.id, save_text)
            self.assertIn("Review." + Rv.id, save_text)
            self.assertIn("State." + St.id, save_text)
            self.assertIn("Amenity." + Am.id, save_text)
            

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        Bm = BaseModel()
        Us = User()
        St = State()
        Pl = Place()
        Cy = City()
        Am = Amenity()
        Rv = Review()
       
        models.storage.new(Am)
        models.storage.new(Rv)
        models.storage.new(Bm)
        models.storage.new(Us)
        models.storage.new(St)
        models.storage.new(Pl)
        models.storage.save()
        models.storage.new(Cy)
        models.storage.reload()
        
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + Bm.id, objs)
        self.assertIn("User." + Us.id, objs)
        self.assertIn("Amenity." + Am.id, objs)
        self.assertIn("Review." + Rv.id, objs)
        self.assertIn("State." + St.id, objs)
        self.assertIn("Place." + Pl.id, objs)
        self.assertIn("City." + Cy.id, objs)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
