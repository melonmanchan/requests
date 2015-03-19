#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Matti's testings for the python requests library."""

## Some path hackery before importing so we can import the right file
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import requests
import pytest
import unittest

class HTTPMethodTestCase(unittest.TestCase):

    def test_simple_get(self):
        r = requests.get("http://google.com")
        assert r.status_code == 200
        assert r.headers['content-type'] == 'text/html; charset=UTF-8'

    def test_simple_post(self):
        payload = {'testkey':'testvalue'}
        r = requests.post("http://httpbin.org/post", params=payload)
        assert r.status_code == 200
        assert "testkey" in r.text

if __name__ == '__main__':
    unittest.main()