#!/usr/bin/python3
import requests
import concurrent.futures
from feature_extraction import Extractor

#debug lib
import gc  
import tracemalloc
import functools

import coloredlogs, logging
coloredlogs.install()
coloredlogs.install(fmt='[%(levelname)s] %(asctime)s: [%(filename)s:%(lineno)d] %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.FileHandler('memory_leak_trace.log', 'w+')
logger.addHandler(ch)

extractor = Extractor()
tracemalloc.start()

# first_log = tracemalloc.take_snapshot()
def _request():
    for _ in range(5):
        logger.info(_)
        first_log = tracemalloc.take_snapshot()
        vector = extractor("https://stackoverflow.com/questions/42179046/what-flavor-of-regex-does-visual-studio-code-use")
        # print(vector)
        second_log = tracemalloc.take_snapshot()
        stats = second_log.compare_to(first_log, 'lineno')
        # for stat in second_log.statistics("lineno"):
        #     logging.info(stat)
            # logger.info(stat)
        for stat in stats[:10]:
            logger.info(stat)

        gc.collect()
        logger.info(gc.collect())
        objects = [i for i in gc.get_objects() 
                if isinstance(i, functools._lru_cache_wrapper)]
        
        for object in objects:
            object.cache_clear()

_request()