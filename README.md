![logo](https://www.brightedge.com/sites/all/themes/custom/brightedge_theme/logo_white.svg)

### Brightedge API
For detailed documentation : [Refer Here](./Brightedge.md)

### Overview of Account Connectors

All account connectors use the **same code** structure. The **configuration file** will vary depending on the specific connector being used.

---

### General Script Description

The script performs the following key actions:
1. **Data Pulling**:  
   - **Timeframe**: The script pulls data between the **last Sunday to Saturday**.
   - **Target Search Engines**:  
     - **Google United Kingdom (GB)** - English (**D**) [1,42]  
     - **Google United Kingdom (GB)** (**S**)  [2,42]
2. **How We Handle Throttling Issues:**
   - We do not pull data from the API directly. Instead, we check the availability of results at different levels (domain, competitor, page, rank). If the results are available, we proceed with pulling the data.
   
   > **Example**: If a domain has 11 pages, we do not pull data for the entire domain at once. Instead, we pull data **page by page**. Additionally, we avoid pulling all data for a page at once.
   
   We pull data based on the following formula:  
   - From rank `((page_num - 1) * 10)` to rank `((page_num - 1) * 10 + 10)`.  
   
   This approach ensures that we retrieve results smoothly and prevent API throttling or breakage.

3. **Error Handling**:  
   The script checks for errors when pulling data. Specifically:
   - **HTTP Errors**: 429 (Too Many Requests), 503 (Service Unavailable), 500 (Internal Server Error)
   - **Retries**: In case of errors, the script attempts to invoke the API up to **three times** before failing.

### Deployment 
If we have to deploy the same birghtedge connector for different account . This is the process we generally follow : 
   - create an empty folder by that account name. 
   - Clone the code from Github repository : https://github.com/Brainlabs-Digital/kingfisher-dashboards-BE-connector.git
   - create the file by name `config.ini` and have the following details :
   ```
   [GENERAL]
SERVICE_ACCOUNT=<path of Service account file of GCP Project>
USERNAME=<Brightedge account username>
PASSWORD=<Brightedge account password>
PROJECT_ID=<Project ID of GCP project>
TABLE_ID=<Table Id where data has to be stored>
SLACK_TOKEN=<Slack token used to publish alerts>
ACCOUNT_ID=<Account ID for which keywords data has to be pulled>
GRANUALARITY_LEVEL=weekly
ACCOUNTS= '{"124009":"BandQ","94906":"screwfix","142607":"tradepoint","285829":"BandQ_IE"}'
```
   - Create a empty folder `Logs` and inside thaty create the empty folder by `<ACCOUNT_NAME>`
   - your scripts are ready to run . To check the manually `python main.py`