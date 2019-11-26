# -*- coding: utf-8 -*-

try:
    import traceback
    import logging
    from sys import exit
    import os
    import re
    import json
    from dao.data_handlers import insert_poi_dataframe
    from libs.soup import save_downloaded_soup
    from libs.address import extract_street_housenumber_better_2, clean_city, \
        clean_javascript_variable, clean_opening_hours_2, clean_phone
    from libs.geo import check_hu_boundary
    from libs.osm import query_postcode_osm_external
    from libs.poi_dataset import POIDataset
except ImportError as err:
    logging.error('Error {0} import module: {1}'.format(__name__, err))
    logging.error(traceback.print_exc())
    exit(128)

POI_DATA = ''


class DataProvider():


    def __init__(self, session, download_cache, prefer_osm_postcode, filetype='', verify_link = True):
        self.session = session
        self.download_cache = download_cache
        self.prefer_osm_postcode = prefer_osm_postcode
        self.filename = '{}.{}'.format(self.__class__.__name__, filetype)
        self.verify_link = verify_link
        self.constains()
        self.data = POIDataset()

    def constains(self):
        self.POI_COMMON_TAGS = ""
        self.link = ''

    def types(self):
        self.__types = []
        return self.__types

    def process(self):
        pass

    def export_list(self):
        if self.data.lenght() < 1:
            logging.warning('Resultset is empty. Skipping ...')
        else:
            insert_poi_dataframe(self.session, self.data.process())
