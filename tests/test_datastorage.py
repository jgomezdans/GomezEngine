import datetime as dt
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

def test_DataStorageSentinel2wrong_band():
    with pytest.raises(AssertionError):
        ds = DataStorageSentinel2("http://www2.geog.ucl.ac.uk/~ucfajlg/Colombia/" +
                               "database.json")
        retval = ds.extract_band("SomeBand")


def test_DataStorageSentinel2wrong_date():
    with pytest.raises(ValueError):
        ds = DataStorageSentinel2("http://www2.geog.ucl.ac.uk/~ucfajlg/Colombia/" +
                               "database.json")
        retval = ds.extract_band("B04", dates=dt.datetime(2002, 2, 2).date())

def test_DataStorageSentinel2_get_all_raster():

    ds = DataStorageSentinel2("http://www2.geog.ucl.ac.uk/~ucfajlg/Colombia/" +
                               "database.json")
    date = dt.datetime(2018, 7, 1).date()
    retval = ds.extract_band("B04", dates=date)
    assert retval["B04"][date].shape == (10980, 10980)

def test_DataStorageSentinel2_get_roi_empty_rastery():
    ds = DataStorageSentinel2("http://www2.geog.ucl.ac.uk/~ucfajlg/Colombia/" +
                               "database.json")
    the_date = dt.datetime(2018, 7, 1).date()
    retval = ds.extract_band("B04", dates=the_date,
                             roi="http://www2.geog.ucl.ac.uk/" +
                             "~ucfajlg/Colombia/aguadas.geojson")
    assert retval["B04"] == {}

def test_DataStorageSentinel2_get_roi_non_empty_rastery():
    ds = DataStorageSentinel2("http://www2.geog.ucl.ac.uk/~ucfajlg/Colombia/" +
                               "database.json")
    #for the_date in list(ds.data_db.keys())[50:60]:
    the_date = dt.datetime(2018, 7, 3).date()
    retval = ds.extract_band("B04", dates=the_date,
                             roi="http://www2.geog.ucl.ac.uk/" +
                             "~ucfajlg/Colombia/aguadas.geojson")
    # The following doesn't pass for GDAL 2.4.0...
    assert retval["B04"][the_date].shape == (1251, 2197)
