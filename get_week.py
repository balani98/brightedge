# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 18:38:01 2024

@author: DeepanshuBalani
"""
import requests
from BEauth import auth_with_BE
import json 
import configparser

Config = configparser.ConfigParser()
Config.read('config.ini')
GET_WEEK_URL='https://api.brightedge.com/3.0/objects/time/124009/weekly/{}'

USERNAME = Config.get('GENERAL','USERNAME')
PASSWORD = Config.get('GENERAL','PASSWORD')
def get_week_of_the_year(first_day_of_the_week):
    username = USERNAME
    password = PASSWORD
    headers = auth_with_BE()
    res = requests.get(url=GET_WEEK_URL.format(first_day_of_the_week), headers=headers, auth=(username, password))
    response = json.loads(res.text) 
    print(response)
    week_of_the_year = response['time_value']
    return week_of_the_year

