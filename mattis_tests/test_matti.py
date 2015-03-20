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

class BasicHTTPMethodTestCase(unittest.TestCase):

    def test_simple_get(self):
        r = requests.get("http://httpbin.org/encoding/utf8")
        assert r.status_code == 200
        assert r.headers['content-type'] == 'text/html; charset=utf-8'

    def test_simple_post(self):
        payload = {'testkey':'testvalue'}
        r = requests.post("http://httpbin.org/post", params=payload)
        assert r.status_code == 200
        assert "testkey" in r.text

    def test_simple_delete(self):
        r = requests.delete("http://httpbin.org/delete")
        assert r.status_code == 200

    def test_simple_put(self):
        payload = {'testkey':'testvalue'}
        r = requests.put("http://httpbin.org/put", params=payload)
        assert r.status_code == 200
        assert "testkey" in r.text

    def test_simple_options(self):
        r = requests.options("http://httpbin.org/post")
        assert r.status_code == 200


class CookiesTestCase(unittest.TestCase):

    def test_setting_session_cookie(self):
        c = requests.session()
        c.get("http://httpbin.org/cookies/set?narsu=maa")
        assert c.cookies['narsu'] == 'maa'

    def test_removing_session_cookie(self):
        c = requests.session()
        c.get("http://httpbin.org/cookies/set?narsu=maa")
        c.get("http://httpbin.org/cookies/delete?narsu")
        with pytest.raises(KeyError):
            c.cookies['narsu'] == 'dasd'

if __name__ == '__main__':
    unittest.main()