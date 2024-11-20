
from apify_client import ApifyClient

# https://console.apify.com/settings/integrations
# compass/Google-Maps-Reviews-Scraper
user_id = 'MDJp6EXVeulZrMc8T'
token ='apify_api_a3J2D0UHuNe8AfDjyEfuhBdOJ7aEEV3dJh4z'



#query https://www.google.com/maps/search/Tel+Aviv-Yafo+restaurants/


# Initialize the ApifyClient with your API token
client = ApifyClient(token)

# Prepare the Actor input
run_input = {
    "startUrls": [{ "url": "https://www.google.com/maps/search/Tel+Aviv-Yafo+restaurants+top+rated/" }],
    "maxReviews": 2,
    "language": "en",
    "personalData": True,
}

# Run the Actor and wait for it to finish
run = client.actor("Xb8osYTtOjlsgI6k9").call(run_input=run_input)

# Fetch and print Actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)