import numpy as np
import os
import pytest
from pytest import fixture
from distutils import dir_util
import urllib.request
from GomezEngine import DataStorage, DataStorageSentinel2

def test_DataStoragewrong_wrong_http():
    #with pytest.raises(urllib.request.URLError):
    with pytest.raises(ValueError):
        ds = DataStorage("htxxx://www.google.com/")


def test_DataStorageSentinel2wrong_http():
    #with pytest.raises(urllib.request.URLError):
    with pytest.raises(ValueError):
        ds = DataStorageSentinel2("htxxx://www.google.com/")

def test_DataStoragewrong_wrong_url():
    #with pytest.raises(urllib.request.URLError):
    with pytest.raises(ValueError):
        ds = DataStorage("http://www2.geog.ucl.ac.uk/nuffink")


def test_DataStorageSentinel2wrong_url():
    #with pytest.raises(urllib.request.URLError):
    with pytest.raises(ValueError):
        ds = DataStorageSentinel2("http://www2.geog.ucl.ac.uk/nuffink")


def test_DataStoragewrong_wrong_json():
    #with pytest.raises(urllib.request.URLError):
    with pytest.raises(OSError):
        ds = DataStorage("http://www2.geog.ucl.ac.uk/~ucfajlg/Colombia/" + 
                         "validate_cloud_optimized_geotiff.py")


def test_DataStorageSentinel2wrong_json():
    #with pytest.raises(urllib.request.URLError):
    with pytest.raises(OSError):
        ds = DataStorageSentinel2("http://www2.geog.ucl.ac.uk/~ucfajlg/Colombia/" + 
                         "validate_cloud_optimized_geotiff.py")
