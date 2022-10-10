from lib import Requester

requester = Requester()

blog = requester.make_api_query(
	handler="blogEntry.view",
	params={"blogEntryId": 87884}
)

import json

print(json.dumps(blog, indent=4))
