# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import zipfile
import os
import re

# TODO: salvar em db
class SaveREADMEPipeline(object):

    def process_item(self, item, spider):

        file_info = item['files'][0]

        with open("%s.README" % file_info['path'], "wb") as f:

            f_csv = csv.DictWriter(f, file_info.keys())

            f_csv.writeheader()
            f_csv.writerow(file_info)

        return item

class UnzipPipeline(object):

    re_file_path = re.compile(r'http://(.*).zip.*')

    def process_item(self, item, spider):

        content_type = item['content_types'][0]

        if content_type == "application/zip":

            file_url = item['file_urls'][0]
            file_info = item['files'][0]
            unzipped_file_path = os.path.join("dataset", UnzipPipeline.re_file_path.findall(file_url)[0].)

            if not os.path.exists(unzipped_file_path):
                os.makedirs(unzipped_file_path)

            with zipfile.ZipFile(file_info['path']) as ziped:
                ziped.extractall(path=unzipped_file_path)

            with open("%s.README" % unzipped_file_path, "wb") as f:

                f_csv = csv.DictWriter(f, file_info.keys())

                f_csv.writeheader()
                f_csv.writerow(file_info)

        return item
