#!/usr/bin/python3
"""Defines unittests for models/amenity.py
"""
import os
import models
import unittest
from datetime import datetime
from models.Amenity import Amenity
from time import sleep


class TestAmenity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Amenity class"""
    def test_new_instance_stored_in_objects(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_no_args_instantiates(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Amenity().id))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_name_is_public_class_attribute(self):
        Am = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", Am.__dict__)

    def test_two_Amenities_different_created_at(self):
        Am1 = Amenity()
        sleep(0.05)
        Am2 = Amenity()
        self.assertLess(Am1.created_at, Am2.created_at)

    def test_two_Amenities_different_updated_at(self):
        Am1 = Amenity()
        sleep(0.05)
        Am2 = Amenity()
        self.assertLess(Am1.updated_at, Am2.updated_at)

    def test_two_amenities_unique_ids(self):
        Am1 = Amenity()
        Am2 = Amenity()
        self.assertNotEqual(Am1.id, Am2.id)

    def test_args_unused(self):
        Am = Amenity(None)
        self.assertNotIn(None, Am.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """instantiation with kwargs test method"""
        Dt = datetime.today()
        Dt_iso = Dt.isoformat()
        Am = Amenity(id="345", created_at=Dt_iso, updated_at=Dt_iso)
        self.assertEqual(Am.id, "345")
        self.assertEqual(Am.created_at, Dt)
        self.assertEqual(Am.updated_at, Dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)

    def test_str_representation(self):
        Dt = datetime.today()
        Dt_repr = repr(Dt)
        Am = Amenity()
        Am.id = "123456"
        Am.created_at = Am.updated_at = Dt
        Amstr = Am.__str__()
        self.assertIn("[Amenity] (123456)", Amstr)
        self.assertIn("'id': '123456'", Amstr)
        self.assertIn("'created_at': " + Dt_repr, Amstr)
        self.assertIn("'updated_at': " + Dt_repr, Amstr)


class TestAmenity_save(unittest.TestCase):
    """Unittests for testing save method of the Amenity class."""
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

    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def test_one_save(self):
        Am = Amenity()
        sleep(0.05)
        first_updated_at = Am.updated_at
        Am.save()
        self.assertLess(first_updated_at, Am.updated_at)

    def test_save_with_arg(self):
        Am = Amenity()
        with self.assertRaises(TypeError):
            Am.save(None)

    def test_save_updates_file(self):
        Am = Amenity()
        Am.save()
        Amid = "Amenity." + Am.id
        with open("file.json", "r") as f:
            self.assertIn(Amid, f.read())

    def test_two_saves(self):
        Am = Amenity()
        sleep(0.05)
        first_updated_at = Am.updated_at
        Am.save()
        second_updated_at = Am.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        Am.save()
        self.assertLess(second_updated_at, Am.updated_at)


class TestAmenity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of Amenity class"""
    def test_to_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_added_attributes(self):
        Am = Amenity()
        Am.middle_name = "Holberton"
        Am.my_number = 98
        self.assertEqual("Holberton", Am.middle_name)
        self.assertIn("my_number", Am.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        Am = Amenity()
        Am_dict = Am.to_dict()
        self.assertEqual(str, type(Am_dict["id"]))
        self.assertEqual(str, type(Am_dict["created_at"]))
        self.assertEqual(str, type(Am_dict["updated_at"]))

    def test_to_dict_contains_correct_keys(self):
        Am = Amenity()
        self.assertIn("id", Am.to_dict())
        self.assertIn("created_at", Am.to_dict())
        self.assertIn("updated_at", Am.to_dict())
        self.assertIn("__class__", Am.to_dict())

    def test_contrast_to_dict_dunder_dict(self):
        Am = Amenity()
        self.assertNotEqual(Am.to_dict(), Am.__dict__)

    def test_to_dict_output(self):
        Dt = datetime.today()
        Am = Amenity()
        Am.id = "123456"
        Am.created_at = Am.updated_at = Dt
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': Dt.isoformat(),
            'updated_at': Dt.isoformat(),
        }
        self.assertDictEqual(Am.to_dict(), tdict)

    def test_to_dict_with_arg(self):
        Am = Amenity()
        with self.assertRaises(TypeError):
            Am.to_dict(None)


if __name__ == "__main__":
    unittest.main()
