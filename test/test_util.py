import unittest
import kovot.util


class DictMock:
    def dict(self):
        return {"hello": "world"}


class UtilTest(unittest.TestCase):
    def test_dict(self):
        x = {"x": None, "y": 1, "z": "value_z",
             "w": DictMock()}
        expected = {"x": None, "y": 1, "z": "value_z",
                    "w": {"hello": "world"}}
        self.assertEqual(kovot.util.dict(x), expected)
