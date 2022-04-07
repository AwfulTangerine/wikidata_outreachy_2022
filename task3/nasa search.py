import requests
from urllib.parse import urlencode
token = "GWyxadCns4nOvfDDthxDP4NloEXkTuWzamSMqPo8"
query = "Near-infrared thermal emission from near-Earth asteroids: Aspect-dependent variability"
encoded_query = urlencode({'q': query, 'fl': 'bibcode'})
print(encoded_query)
results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query), \
                       headers={'Authorization': 'Bearer ' + token})
# format the response in a nicely readable format
print(list(results.json()['response']['docs'][0].values())[0])