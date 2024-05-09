# -*- coding: utf-8 -*-
"""
Created on Thu May  9 12:02:14 2024

@author: DeepanshuBalani
"""
from main import pull_data
import datetime
import time
from logger import setup_logging
import logging
def invoke_the_API():
    i=1
    file_logger = setup_logging('Logs/'+ account_name + '/' + account_name + '_'+'overall_logs.log', logging.DEBUG)
    start_date= datetime.datetime(2023, 1, 1)
    end_date = datetime.datetime(2023, 1, 7)
    for i in range(27):
        start_date_str = start_date.strftime('%Y%m%d')
        end_date_str = end_date.strftime('%Y%m%d')
        file_logger.debug("running for "+ start_date_str +  "and" + end_date_str )
        pull_data(start_date_str,end_date_str)
        file_logger.debug("finished for "+ start_date_str +  "and" + end_date_str )
        start_date.add(days=7)
        end_date.add(days=7)
        print(start_date,end_date)
        file_logger.debug("sleeping for a hour" )
        time.sleep(3600)
    file_logger.log("finished the running for 26 weeks till "+end_date_str)
invoke_the_API()
        