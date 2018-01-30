#! /usr/bin/env python
# coding:utf-8


class ModInterfaceTestMixin:
    def test_implements_mod_interface(self):
        self.assertTrue(hasattr(self.object, "is_available"))
        self.assertTrue(hasattr(self.object, "get_responses"))
