#!/usr/bin/python3
"""Defines unittests for models/city.py.

Unittest classes:
    TestCity_instantiation
    TestCity_save
    TestCity_to_dict
"""
import os
import models
import unittest
from time import sleep
from models.City import City
from datetime import datetime

class TestCity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_id_is_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_no_args_instantiates(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_name_is_public_class_attribute(self):
        Cy = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(Cy))
        self.assertNotIn("name", Cy.__dict__)
    
    def test_state_id_is_public_class_attribute(self):
        Cy = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(Cy))
        self.assertNotIn("state_id", Cy.__dict__)

    def test_two_cities_unique_ids(self):
        Cy1 = City()
        Cy2 = City()
        self.assertNotEqual(Cy1.id, Cy2.id)

    def test_two_cities_different_updated_at(self):
        Cy1 = City()
        sleep(0.05)
        Cy2 = City()
        self.assertLess(Cy1.updated_at, Cy2.updated_at)

    def test_two_cities_different_created_at(self):
        Cy1 = City()
        sleep(0.05)
        Cy2 = City()
        self.assertLess(Cy1.created_at, Cy2.created_at)

    def test_instantiation_with_kwargs(self):
        Dt = datetime.today()
        Dt_iso = Dt.isoformat()
        Cy = City(id="345", created_at=Dt_iso, updated_at=Dt_iso)
        self.assertEqual(Cy.id, "345")
        self.assertEqual(Cy.created_at, Dt)
        self.assertEqual(Cy.updated_at, Dt)

    def test_str_representation(self):
        Dt = datetime.today()
        Dt_repr = repr(Dt)
        Cy = City()
        Cy.id = "123456"
        Cy.created_at = Cy.updated_at = Dt
        Cystr = Cy.__str__()
        self.assertIn("[City] (123456)", Cystr)
        self.assertIn("'id': '123456'", Cystr)
        self.assertIn("'created_at': " + Dt_repr, Cystr)
        self.assertIn("'updated_at': " + Dt_repr, Cystr)

    def test_args_unused(self):
        Cy = City(None)
        self.assertNotIn(None, Cy.__dict__.values())

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """Unittests for testing save method of the City class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_save_updates_file(self):
        Cy = City()
        Cy.save()
        Cyid = "City." + Cy.id
        with open("file.json", "r") as x:
            self.assertIn(Cyid, x.read())

    def test_two_saves(self):
        Cy = City()
        sleep(0.05)
        first_updated_at = Cy.updated_at
        Cy.save()
        second_updated_at = Cy.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        Cy.save()
        self.assertLess(second_updated_at, Cy.updated_at)

    def test_one_save(self):
        Cy = City()
        sleep(0.05)
        first_updated_at = Cy.updated_at
        Cy.save()
        self.assertLess(first_updated_at, Cy.updated_at)

    def test_save_with_arg(self):
        Cy = City()
        with self.assertRaises(TypeError):
            Cy.save(None)

class TestCity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_added_attributes(self):
        Cy = City()
        Cy.middle_name = "Holberton"
        Cy.my_number = 98
        self.assertEqual("Holberton", Cy.middle_name)
        self.assertIn("my_number", Cy.to_dict())

    def test_to_dict_contains_correct_keys(self):
        Cy = City()
        self.assertIn("id", Cy.to_dict())
        self.assertIn("created_at", Cy.to_dict())
        self.assertIn("updated_at", Cy.to_dict())
        self.assertIn("__class__", Cy.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        Cy = City()
        Cy_dict = Cy.to_dict()
        self.assertEqual(str, type(Cy_dict["id"]))
        self.assertEqual(str, type(Cy_dict["created_at"]))
        self.assertEqual(str, type(Cy_dict["updated_at"]))

    def test_to_dict_output(self):
        Dt = datetime.today()
        Cy = City()
        Cy.id = "123456"
        Cy.created_at = Cy.updated_at = Dt
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': Dt.isoformat(),
            'updated_at': Dt.isoformat(),
        }
        self.assertDictEqual(Cy.to_dict(), tdict)

    def test_to_dict_with_arg(self):
        Cy = City()
        with self.assertRaises(TypeError):
            Cy.to_dict(None)

    def test_contrast_to_dict_dunder_dict(self):
        Cy = City()
        self.assertNotEqual(Cy.to_dict(), Cy.__dict__)

if __name__ == "__main__":
    unittest.main()