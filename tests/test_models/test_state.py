#!/usr/bin/python3
"""Defines unittests for models/state.py
"""
import os
import models
import unittest
from time import sleep
from models.State import State
from datetime import datetime

class TestState_instantiation(unittest.TestCase):
    """Unittests for testing """

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(State()))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_name_is_public_class_attribute(self):
        St = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(St))
        self.assertNotIn("name", St.__dict__)

    def test_two_states_unique_ids(self):
        St1 = State()
        St2 = State()
        self.assertNotEqual(St1.id, St2.id)

    def test_str_representation(self):
        Dt = datetime.today()
        Dt_repr = repr(Dt)
        St = State()
        St.id = "123456"
        St.created_at = St.updated_at = Dt
        StStr = St.__str__()
        self.assertIn("[State] (123456)", StStr)
        self.assertIn("'id': '123456'", StStr)
        self.assertIn("'created_at': " + Dt_repr, StStr)
        self.assertIn("'updated_at': " + Dt_repr, StStr)

    def test_two_states_different_created_at(self):
        St1 = State()
        sleep(0.05)
        St2 = State()
        self.assertLess(St1.created_at, St2.created_at)

    def test_two_states_different_updated_at(self):
        St1 = State()
        sleep(0.05)
        St2 = State()
        self.assertLess(St1.updated_at, St2.updated_at)

    def test_args_unused(self):
        St = State(None)
        self.assertNotIn(None, St.__dict__.values())

    def test_instantiation_with_kwargs(self):
        Dt = datetime.today()
        Dt_iso = Dt.isoformat()
        St = State(id="345", created_at=Dt_iso, updated_at=Dt_iso)
        self.assertEqual(St.id, "345")
        self.assertEqual(St.created_at, Dt)
        self.assertEqual(St.updated_at, Dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """Unittests for testing """

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

    def test_one_save(self):
        St = State()
        sleep(0.05)
        first_updated_at = St.updated_at
        St.save()
        self.assertLess(first_updated_at, St.updated_at)

    def test_two_saves(self):
        St = State()
        sleep(0.05)
        first_updated_at = St.updated_at
        St.save()
        second_updated_at = St.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        St.save()
        self.assertLess(second_updated_at, St.updated_at)

    def test_save_with_arg(self):
        St = State()
        with self.assertRaises(TypeError):
            St.save(None)

    def test_save_updates_file(self):
        St = State()
        St.save()
        Stid = "State." + St.id
        with open("file.json", "r") as f:
            self.assertIn(Stid, f.read())

class TestState_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method """

    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))
    
    def test_to_dict_contains_added_attributes(self):
        St = State()
        St.middle_name = "Holberton"
        St.my_number = 98
        self.assertEqual("Holberton", St.middle_name)
        self.assertIn("my_number", St.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        St = State()
        St_dict = St.to_dict()
        self.assertEqual(str, type(St_dict["id"]))
        self.assertEqual(str, type(St_dict["created_at"]))
        self.assertEqual(str, type(St_dict["updated_at"]))

    def test_to_dict_contains_correct_keys(self):
        St = State()
        self.assertIn("id", St.to_dict())
        self.assertIn("created_at", St.to_dict())
        self.assertIn("updated_at", St.to_dict())
        self.assertIn("__class__", St.to_dict())

    def test_to_dict_output(self):
        Dt = datetime.today()
        St = State()
        St.id = "123456"
        St.created_at = St.updated_at = Dt
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': Dt.isoformat(),
            'updated_at': Dt.isoformat(),
        }
        self.assertDictEqual(St.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        St = State()
        self.assertNotEqual(St.to_dict(), St.__dict__)

    def test_to_dict_with_arg(self):
        St = State()
        with self.assertRaises(TypeError):
            St.to_dict(None)

if __name__ == "__main__":
    unittest.main()
