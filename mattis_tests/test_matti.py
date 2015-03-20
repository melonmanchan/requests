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

from PIL import Image, ImageChops
from StringIO import StringIO
import os.path

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


class SessionsTestCase(unittest.TestCase):

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

    def test_basic_session_auth(self):
        auth = ('user', 'pass')
        url = "http://httpbin.org/basic-auth/user/pass"
        r = requests.get(url, auth=auth)
        assert r.status_code == 200
        r = requests.get(url)
        assert r.status_code == 401

    def test_digest_auth_session(self):
        auth = requests.auth.HTTPDigestAuth('user', 'pass')
        url = "http://httpbin.org/digest-auth/auth/user/pass"
        c = requests.session()
        c.get(url, auth=auth)
        assert c.cookies['fake'] == 'fake_value'


class ExceptionTestCase(unittest.TestCase):

    def test_bad_urls(self):
        with pytest.raises(requests.exceptions.MissingSchema):
            requests.get("asdsadadsasfasfcxvcxv")

        with pytest.raises(requests.exceptions.InvalidSchema):
            requests.get("localhost:3124")

        with pytest.raises(requests.exceptions.InvalidURL):
            requests.get('http://')

    def test_invalid_domains_and_ports(self):
        with pytest.raises(requests.exceptions.ConnectionError):
            requests.get("http://hiiohoihalojatapaivaa.jamk.fi")
        with pytest.raises(requests.exceptions.ConnectionError):
            requests.get("http://jamk.fi:1337", timeout=1)

    def test_exception_rise(self):
        bad_r = requests.get("http://httpbin.org/status/404")
        with pytest.raises(requests.exceptions.HTTPError):
            bad_r.raise_for_status()

    def test_timeout(self):
        with pytest.raises(requests.exceptions.Timeout):
            requests.get("http://httpbin.org/delay/2", timeout=1)

class FileHandlingTestCase(unittest.TestCase):

    def test_jpg_download(self):
        r = requests.get("http://httpbin.org/image/jpeg")
        image1 = Image.open(StringIO(r.content))
        image2 = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "jpeg.jpg"))
        assert ImageChops.difference(image1, image2).getbbox() is None

    def test_png_download(self):
        r = requests.get("http://httpbin.org/image/png")
        image1 = Image.open(StringIO(r.content))
        image2 = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "png.png"))
        assert ImageChops.difference(image1, image2).getbbox() is None
        
if __name__ == '__main__':
    unittest.main()