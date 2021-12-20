import os
import grpc
import time
import random
import pymongo
import threading
import json
# page_data.sections.SECTION_RES_DETAILS.HIGHLIGHTS.highlights

with open("zmt.json", "rb") as f:
    js = json.loads(f.read())
    for i in js['page_data']['sections']['SECTION_RES_DETAILS']['HIGHLIGHTS']['highlights']:
        if i['type'] == 'AVAILABLE':
            print(i)
