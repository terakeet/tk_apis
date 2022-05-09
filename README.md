# TK APIs

This is a collection of the wrapper functions used to call various third-party,
SERP-related data sources. The implementation returns things as 
[Pandas DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html),
because this package was written by a data scientist for data science use.

## Code examples

The package contains modules for each of the APIs. 
You'll need to provide your own API keys; an easy way to do this is a `.env` file. 

My examples below assume you have defined a `.env` and use the `python-dotenv` package to 
load in this information:

```angular2html
from dotenv import load_dotenv
import os

load_dotenv()
```

Once the credentials are in, you can load the desired module(s) and execute queries accordingly:

### Moz
```angular2html
from tk_apis import moz_calls as moz

moz.get_domain_authority(url='https://www.terakeet.com', 
                         api_key=os.environ['MOZ_AUTH'])
```

### SemRush
```angular2html
from tk_apis import semrush_calls as sr

sr.get_keyword_data(keyword='babylonian empire', 
                    api_key=os.environ['SEMRUSH_KEY'])
sr.get_organic_results(keyword='babylonian empire',
                       api_key=os.environ['SEMRUSH_KEY'],
                       n=10)
sr.get_search_volume(keyword='sumerians', 
                     api_key=os.environ['SEMRUSH_KEY'])
```

### SerpApi
```angular2html
from tk_apis import serpapi_calls as sa

serp = sa.get_serp_result(keyword='arnold schwarzenegger', 
                          api_key=os.environ['SERPAPI_KEY'])
sa.extract_organic_df(result_set=serp)
sa.extract_knowledge_graph(result_set=serp)
sa.extract_top_stories(result_set=serp)
sa.extract_related_searches(result_set=serp)
sa.extract_related_questions(result_set=serp)
```