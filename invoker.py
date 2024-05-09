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
import json
import ast
import configparser
Config = configparser.ConfigParser()
Config.read('config.ini')
SERVICE_ACCOUNT = Config.get('GENERAL', 'SERVICE_ACCOUNT')
PROJECT_ID = Config.get('GENERAL','PROJECT_ID')
TABLE_ID = Config.get('GENERAL','TABLE_ID')
USERNAME = Config.get('GENERAL','USERNAME')
PASSWORD = Config.get('GENERAL','PASSWORD')
SLACK_TOKEN =  Config.get('GENERAL','SLACK_TOKEN')
ACCOUNT_ID =  Config.get('GENERAL','ACCOUNT_ID')
ACCOUNTS = Config.get("GENERAL", "ACCOUNTS")
def get_account_name():
    print(ACCOUNTS)
    accounts_json = json.loads(ast.literal_eval(ACCOUNTS))
    account_id_str = str(ACCOUNT_ID)
    account = accounts_json[account_id_str]
    return account

def invoke_the_API():
    account_name = get_account_name()
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
        