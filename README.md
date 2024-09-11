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

If we need to deploy the same BrightEdge connector for different accounts, follow this process:

1. **Create a new folder**:
   - Create an empty folder named after the account.

2. **Clone the repository**:
   - Clone the code from the GitHub repository:  
     [https://github.com/Brainlabs-Digital/kingfisher-dashboards-BE-connector.git](https://github.com/Brainlabs-Digital/kingfisher-dashboards-BE-connector.git)

3. **Create the `config.ini` file**:
   - Inside the new folder, create a file named `config.ini` with the following content:
   ```ini
   [GENERAL]
   SERVICE_ACCOUNT=<path of Service account file of GCP Project>
   USERNAME=<BrightEdge account username>
   PASSWORD=<BrightEdge account password>
   PROJECT_ID=<Project ID of GCP project>
   TABLE_ID=<Table Id where data has to be stored>
   SLACK_TOKEN=<Slack token used to publish alerts>
   ACCOUNT_ID=<Account ID for which keywords data has to be pulled>
   GRANULARITY_LEVEL=weekly
   ACCOUNTS= '{"124009":"BandQ","94906":"screwfix","142607":"tradepoint","285829":"BandQ_IE"}'

4. Create an empty folder `Logs` and inside that, create a subfolder named `<ACCOUNT_NAME>`.
5. Your scripts are now ready to run. To run them manually, execute: `python main.py`.
6. Now comes the scheduling part of the above script. Copy the path of `main.py` from the above folder, and open the crontab with `sudo crontab -e`. Add the following line at the end:

  ```bash
  * * * * * /usr/bin/python3 <path_to_main.py> >> <path_to_log_file> 2>&1