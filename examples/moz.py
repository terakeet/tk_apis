from tk_apis import MOZAPI

# initalize the wrapper class
moz = MOZAPI()

# declare your URL list you'd like to get data for
urls = ["example.com"]

# set your parameters
p = {"daily_history_values": ["domain_authority", "page_authority"]}
# make the API request
data = moz.url_metrics(urls, params=p)

# format the response as a pandas DataFrame (without the history columns)
raw_df = moz.format_response(data)
