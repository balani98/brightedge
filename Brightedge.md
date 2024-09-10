
![logo](https://www.brightedge.com/sites/all/themes/custom/brightedge_theme/logo_white.svg)

## BrightEdge API
Brightedge is a leading SEO solution and content marketing platform that transforms online content such as traffic , revenue and engagement into tangible business results . It provides realtime research recommendation and rankings . Brightedge platform is powered by an Artificial intelligence , Datamind which is capable of web-wide,real time measurement of digital content engagement across all digital channels including search , social and mobile . 

### Primary usecases
**Use this connector to pull data about search engine optimization** 

### Primary key metrics 
- keyword rankings 
- competitor rankings 
- search volume 
- Tracked searches 

Brightedge provides you following reports:


**Accounts :** Retrieves list of all accounts 

**Competitors :** Retrieves list of all competitors being tracked for your account.

**Domains :** Retrieves list of all domains tracked for your account . 

**Keywords :** Retrieves list of all keywords being tracked for your account.

**Keyword Groups :** Retrieves list of all keyword groups being tracked for your account.

**Search Engines :** Retrieves list of all search engines that are enabled for specific account . 



In this project we are leveraging Brightedge API 3.0 . Brightedge divides the APIs into different datasets. To query the datasets we have to use query with Brightedge query language (BQL) which looks like JSON . Each dataset has different fields to query . 

>For Ex- If we have to extract the keywords specific to domain . we have to query against this URL : https://api.brightedge.com/3.0/query/124009 with this BQL .

```
query={
"dataset": "keyword",
"dimension": ["keyword", "page_url", "time","domain","search_engine"],
"measures": ["rank", "page_num", "search_volume"],
"dimensionOptions": {
"time": 'weekly'
},
"filter": [
["time", "eq", week_of_the_year],
["search_engine",[search_engine]],
["search_volume","gt",50],
["is_my_domain","eq",1],
],
"order":[["search_volume","desc"]],
"count": 1,
"offset":0
}
```

For detailed documentation and integration instructions, please refer to the official Brightedge documentation .
[Refer Here](./API-user-guide.pdf) 
