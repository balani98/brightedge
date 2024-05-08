import requests
import json
from BEauth import auth_with_BE
import json
import pandas as pd
import time
import time
import pandas_gbq
from google.oauth2 import service_account
import pandas as pd
import datetime
from datetime import timedelta
from get_week import get_week_of_the_year
from logger import setup_logging
import logging
import configparser
from slack_sdk import WebClient
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
BE_API_URL = 'https://api.brightedge.com/3.0/query/124009'

Config = configparser.ConfigParser()
Config.read('config.ini')
SERVICE_ACCOUNT = Config.get('GENERAL', 'SERVICE_ACCOUNT')
PROJECT_ID = Config.get('GENERAL','PROJECT_ID')
TABLE_ID = Config.get('GENERAL','TABLE_ID')
USERNAME = Config.get('GENERAL','USERNAME')
PASSWORD = Config.get('GENERAL','PASSWORD')
SLACK_TOKEN =  Config.get('GENERAL','SLACK_TOKEN')

# Set up a WebClient with the Slack OAuth token
client = WebClient(token=SLACK_TOKEN)

def push_to_bq(df, project_id, table_id, service_account_key_path):
    df['time'] = df['time'].astype(str)
    schema = [
    {'name': 'keyword', 'type': 'STRING'},
    {'name': 'page_num', 'type': 'INT64'},
    {'name': 'search_vlume', 'type': 'INT64'},
    {'name': 'rank', 'type': 'INT64'},
    {'name': 'time', 'type': 'STRING'},
    {'name': 'page_url', 'type': 'STRING'},
    {'name': 'search_engine', 'type': 'STRING'},
    {'name': 'time_period', 'type': 'STRING'},
    {'name': 'first_day_of_week', 'type': 'DATE'},
    
    ]
    #convert_dict = {'keyword':str,'page_num':int,'search_engine':str,'search_volume':int, 'rank':int,'time':str,'page_url':str,'time_period':str,'first_day_of_week':datetime}
    #dframe = df.astype(convert_dict)
    credentials = service_account.Credentials.from_service_account_file(service_account_key_path)
    # Assuming your DataFrame is named 'df'
    # Push the DataFrame to BigQuery
    pandas_gbq.to_gbq(df, table_id, project_id=project_id, if_exists='append', credentials=credentials)
    print("pushed to BQ")

@retry( wait=wait_fixed(200), retry=retry_if_exception_type(requests.exceptions.HTTPError),
       stop=stop_after_attempt(3),
       reraise=True)
def get_total_number_of_keyword_results(logger,week_of_the_year, page_no=None, rank=None):
    query = {}
    if page_no is None:
        query={
        "dataset": "keyword",
        "dimension": ["keyword", "page_url", "time","domain","search_engine"],
        "measures": ["rank", "page_num", "search_volume"],
        "dimensionOptions": {
            "time": "weekly"
        },
        "filter": [
            ["time", "eq", week_of_the_year],
            ["search_engine",[[1,42]]],
            ["search_volume","gt",50],
            ["is_my_domain","eq",1],
        ],
        "order":[["search_volume","desc"]],
        "count": 1,
        "offset":0
    }
    elif rank is None:
        query={
        "dataset": "keyword",
        "dimension": ["keyword", "page_url", "time","domain","search_engine"],
        "measures": ["rank", "page_num", "search_volume"],
        "dimensionOptions": {
            "time": "weekly"
        },
        "filter": [
            ["time", "eq", week_of_the_year],
            ["search_engine",[[1,42]]],
            ["search_volume","gt",50],
            ["is_my_domain","eq",1],
            ["page_num","eq",page_no]
        ],
        "order":[["search_volume","desc"]],
        "count": 1,
        "offset":0
    }
    else:
        query={
        "dataset": "keyword",
        "dimension": ["keyword", "page_url", "time","domain","search_engine"],
        "measures": ["rank", "page_num", "search_volume"],
        "dimensionOptions": {
            "time": "weekly"
        },
        "filter": [
            ["time", "eq", week_of_the_year],
            ["search_engine",[[1,42]]],
            ["rank","eq", rank],
            ["search_volume","gt",50],
            ["is_my_domain","eq",1],
            ["page_num","eq",page_no]
        ],
        "order":[["search_volume","desc"]],
        "count": 1,
        "offset":0
    }

    print(query)
    # extracitng the headers
    headers = auth_with_BE()
    # Convert payload to JSON string
    payload_json = json.dumps(query)
    raw_text="query="+payload_json
    response = requests.post(BE_API_URL, headers=headers, auth=(USERNAME, PASSWORD), data=raw_text,timeout=700.0)
    # Raise excpetion only in case of 500 error.
    if response.status_code == 503 or response.status_code == 504:
        logger.debug("Try failed")
        response.raise_for_status()
        
    res_json = json.loads(response.text)
    total_results = res_json['total']
    return total_results

@retry(wait=wait_fixed(200),
       retry=retry_if_exception_type(requests.exceptions.HTTPError),
       stop=stop_after_attempt(3),
       reraise=True)
def get_keyword_results(logger,week_of_the_year, page_no, rank):
    query = {
    "dataset": "keyword",
    "dimension": ["keyword", "page_url", "time","domain","search_engine"],
    "measures": ["rank", "page_num", "search_volume"],
    "dimensionOptions": {"time": "weekly"},
    "filter": [["time","eq",week_of_the_year],
               ["search_engine",[[1,42]]],
               ["rank","eq",rank],
               ["search_volume","gt",50],
               ["is_my_domain","eq",1],
               ["page_num","eq",page_no]
              ],
    "order":[["search_volume","desc"]],
    "count": 10000,
    "offset": 0    
    }
    print(query)
    # extracitng the headers
    headers = auth_with_BE()
    # Convert payload to JSON string
    payload_json = json.dumps(query)
    raw_text="query="+payload_json
    response = requests.post(BE_API_URL, headers=headers, auth=(USERNAME, PASSWORD), data=raw_text,timeout=700.0)
    if response.status_code == 503 or response.status_code == 504:
        logger.debug("Try failed")
        response.raise_for_status()
    #print("res",response.text)
    res_json = json.loads(response.text)
    return res_json




def pull_data():
    try:
        # Start time
        start_time = time.time()
        # Get today's date
        today = datetime.datetime.today()
        
        # Subtract 7 days
        seven_days_ago = today - timedelta(days=7)
        one_day_ago = today - timedelta(days=1)
        # Format the date as yyyymmdd
        #first_day_of_the_week = seven_days_ago.strftime('%Y%m%d')
        #last_day_of_the_week = one_days_ago.strftime('%Y%m%d')
        first_day_of_the_week = '20240331'
        converted_first_day_of_week = datetime.datetime.strptime(first_day_of_the_week,
                                '%Y%m%d').strftime("%d %b %Y")
        last_day_of_the_week = '20240406'
        converted_last_day_of_week = datetime.datetime.strptime(last_day_of_the_week,
                                '%Y%m%d').strftime("%d %b %Y")
        first_day_of_week_specific_format = datetime.datetime(int(first_day_of_the_week[0:4]), int(first_day_of_the_week[4:6]), int(first_day_of_the_week[6:8]))
        week_of_the_year = get_week_of_the_year(first_day_of_the_week)
        file_logger = setup_logging('Logs/log_'+week_of_the_year+'.log', logging.DEBUG)
        file_logger.debug("Script execution has been started on time".format(start_time))
        
        
        week_no = week_of_the_year[-2:]
        message="data pull is started for start date {} and last date {}".format(first_day_of_the_week,last_day_of_the_week)
        client.chat_postMessage(
            channel="kingfisher-data-pull-alerts", 
            text=message, 
            username="Bot User"
         )
        file_logger.debug("data pull is started for start date {} and last date {}".format(first_day_of_the_week,last_day_of_the_week))
        file_logger.debug("this data pull is started for week {}".format(week_of_the_year))
        
        total_results_for_domain =  get_total_number_of_keyword_results(file_logger, week_of_the_year)
        file_logger.debug("total results for this domain for {} are {}".format(week_of_the_year,total_results_for_domain))
        print("total results needed", total_results_for_domain)
        results_domain_level=0
        page_no=1
        
        while True:
            rank = (page_no-1)*10
            total_results_for_page = get_total_number_of_keyword_results(file_logger, week_of_the_year, page_no)
            print("tot res", total_results_for_page)
            file_logger.debug("started the script for page {}".format(page_no))
            file_logger.debug("Total results for page {} are {}".format(page_no, total_results_for_page))
            
            results=0
            if total_results_for_page != 0:
                while True:
                    file_logger.debug("started the script for page {} and rank {}".format(page_no,rank))
                    
                    df = pd.DataFrame()
                    total_results_for_page_for_rank = get_total_number_of_keyword_results(file_logger,week_of_the_year, page_no, rank)
                    file_logger.debug("Total results for page {} and rank {} are {}".format(page_no,rank,total_results_for_page_for_rank))
                    
                    if total_results_for_page_for_rank != 0:
                        kw_response = get_keyword_results(file_logger,week_of_the_year, page_no, rank)
                        kw_results = kw_response['values']
                        df_keyword = pd.DataFrame(kw_results)
                        # create the new column time period
                        df_keyword["time_period"] = str(converted_first_day_of_week) + " to " + str(converted_last_day_of_week) + " Week ( " + str(week_no) + " )"
                        df_keyword["first_day_of_week"] = pd.to_datetime(first_day_of_week_specific_format)
                        push_to_bq(df_keyword, PROJECT_ID, TABLE_ID, SERVICE_ACCOUNT)
                        file_logger.debug("pushed the results for rank page {} and rank {}".format(page_no, rank))
                        print("pushed the results for rank page {} and rank {}",page_no, rank)
                        results += kw_response['total']
                        results_domain_level += results 
                        file_logger.debug("remaining records for page {} are {}".format(page_no, total_results_for_page-results))
                        print("remaining records for page {} are {}",page_no, total_results_for_page-results)
                        if results ==  total_results_for_page or page_no*10==rank:
                            break
                    rank = rank+1
                    time.sleep(5)
                    print("sleeping for 5 seconds after each API call")
            print("remaining records for domain {}" ,total_results_for_domain-results_domain_level)
            if results_domain_level == total_results_for_domain or page_no==10:
                break
            time.sleep(120)
            print("sleeping for 120 seconds after each page completion")
            page_no = page_no + 1
            print("end page", page_no)
        end_time = time.time()
        # Calculate execution time
        execution_time = end_time - start_time
        
        # Display execution time
        print("Execution time:", execution_time, "seconds")
        message="data pull is completed for start date {} and last date {}".format(first_day_of_the_week,last_day_of_the_week)
        client.chat_postMessage(
           channel="kingfisher-data-pull-alerts", 
           text=message, 
           username="Bot User"
        )
    except Exception as error:
        error_message = "data pull is failed due to "+ str(error)  +" for start date {} and last date {}".format(first_day_of_the_week,last_day_of_the_week)
        print(error_message)
        client.chat_postMessage(
           channel="kingfisher-data-pull-alerts", 
           text=error_message, 
           username="Bot User"
        )
pull_data()