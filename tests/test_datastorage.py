import numpy as np
import os
import pytest
from pytest import fixture
from distutils import dir_util
import urllib.request
from GomezEngine import DataStorage, DataStorageSentinel2

def test_DataStoragewrong_url():
    #with pytest.raises(urllib.request.URLError):
    with pytest.raises(ValueError):
        ds = DataStorage("htxxx://www.google.com/")


def test_DataStorageSentinel2wrong_url():
    #with pytest.raises(urllib.request.URLError):
    with pytest.raises(ValueError):
        ds = DataStorageSentinel2("htxxx://www.google.com/")
