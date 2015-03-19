#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Matti's testings for the python requests library."""

## Some path hackery before importing so we can import the right file
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import requests
import pytest

class MattiTestClass:
    def test_one(self):
        x = "hello"
        assert 'h' in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, 'check')