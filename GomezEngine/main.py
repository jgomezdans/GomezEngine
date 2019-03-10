#!/usr/bin/env python

import json
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed

import datetime as dt

import urllib.request

from collections import defaultdict

import numpy as np

from tqdm.autonotebook import tqdm


from osgeo import gdal

gdal.UseExceptions()



def retrieve_field(k, band, url0, roi=None, urlcloud=None, cld_thresh=20):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if roi is not None:
            if roi.find("http://") >= 0:
                prefix = "/vsicurl/"
            else:
                prefix = ""
            kwds={"cutlineDSName":f"{prefix:s}{roi}",
                              "cropToCutline":True}
        else:
            kwds = {}
        g1 = gdal.Warp("", f"/vsicurl/{url0:s}", format="MEM", **kwds)
        if urlcloud is not None:
            height = g1.RasterYSize
            width = g1.RasterXSize
            g = gdal.Warp("", f"/vsicurl/{urlcloud:s}", format="MEM",
                          height=height, width=width, **kwds)
            cld = g.ReadAsArray()
            if np.sum(cld < cld_thresh) == 0:
                # No clear pixels
                return k, band, None        
        data1 = g1.ReadAsArray()*1.
        data1[data1 < -9990] = np.nan
        if urlcloud is not None:
            data1[cld > cld_thresh] = np.nan
        if np.isnan(np.nanmean(data1)):
            return k, band, None
        return k, band, data1



class DataStorage(object):
    def __init__(self, url, max_workers=10):
        try:
            remote_file = urllib.request.urlopen(url)
        except urllib.request.HTTPError as e:
            raise ValueError("Can't connect. Reason " + 
                                f"{e.msg:s}")
        except urllib.request.URLError as e:
            raise ValueError("Can't connect. Reason " + 
                                f"{e.reason:s}")        
        try:
            tmp_db = json.loads(remote_file.read())
        except json.JSONDecodeError:
            raise IOError("Remote json file appears dodgy")
        dates = [
            (k, dt.datetime.strptime(k, "%Y-%m-%d").date())
            for k in tmp_db.keys()
        ]
        self.data_db = {kk: tmp_db[k] for (k, kk) in dates}
        self.max_workers = max_workers

class DataStorageSentinel2(DataStorage):
    def __init__(self, url):
        DataStorage.__init__(self, url, max_workers=10)
        self.valid_bands = [
            "B02",
            "B03",
            "B04",
            "B05",
            "B06",
            "B07",
            "B08",
            "B8A",
            "B11",
            "B12",
            "CLD",
            "AOT",
            "TCWV",
        ]
        
    def extract_band(self, bands, dates=None, roi=None, use_cloud_mask=True,
                            cld_thresh=20):
        if type(bands) != type([]): bands = [bands]
        assert all([band in self.valid_bands for band in bands])
        
        sel_dates = list(self.data_db.keys()) if dates is None else dates
        if type(sel_dates) != type([]): sel_dates = [sel_dates]
        not_present = list((set(sel_dates).difference(set(
                self.data_db.keys()))))
            
        if len(not_present)  != 0:
                raise ValueError(f"{str(not_present):s} not present in DB!")
        with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
            futures = []
            for band in bands:
                band_loc = self.valid_bands.index(band)
                for k in sel_dates:
                    if use_cloud_mask:
                        cld_file = [s for s in self.data_db[k] 
                                if s.endswith("_CLD.vrt")][0]
                    else:
                        cld_file = None
                    futures.append(ex.submit(retrieve_field, k,
                                             band, self.data_db[k][band_loc],
                                             roi, urlcloud=cld_file, 
                                             cld_thresh=cld_thresh))
            kwargs = {
                'total': len(futures),
                'unit': 'it',
                'unit_scale': True,
                'leave': True
            }
            analysis_data = defaultdict(dict)
            #Print out the progress as tasks complete
            for f in tqdm(as_completed(futures), **kwargs):
                f0, f1, f2  = f.result()
                analysis_data[f1][f0] = f2
        clean_data = {}
        for band in bands:
            clean_data[band] = {k:v for k,v in analysis_data[band].items() 
                                if v is not None}
        return clean_data
