import foursquare
from foursquare_accounts import accounts

app = accounts["tutorial"]

client = foursquare.Foursquare(client_id=app["client_id"],
                               client_secret=app["client_secret"])

client.set_access_token(app["access_token"])

results = client.venues.search({"query": "candy", "ll": "45.507297, -73.565469"})

for result in results["venues"]:
	print(result["name"])