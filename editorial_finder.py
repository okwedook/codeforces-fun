from lib import Requester
import json
import re
import time
import sys

requester = Requester()

contests = requester.make_api_query("contest.list", {})['result']

editorialIdsFile = open("editorial_ids.txt", "w")

for contest in contests:
	if contest["startTimeSeconds"] > time.time():
		continue
	contest_page = requester.make_raw_query(f"contest/{contest['id']}")
	print(f"Current contest: {contest['id']}")
	found = 0
	for line in contest_page.split('\n'):
		line = str(line)
		if any(text in line for text in ["Editorial", "Tutorial", "Разбор"]) and "href=\"/blog/entry/" in line:
			try:
				match = re.match(".*/blog/entry/(\\d+)[^\\d]", line)
				editorial_blog_id = int(match.group(1))
				editorialIdsFile.write(f"{contest['id']} {editorial_blog_id}\n")
				editorialIdsFile.flush()
				found += 1
			except Exception as e:
				pass
	if found == 0:
		print(f"Editorial not found for {contest['name']}")
	if found > 1:
		print(f"Multiple editorials found for {contest['name']}")
	sys.stdout.flush()


# import requests

# response = requests.get("https://codeforces.com/contest/1737")

# for line in response:
# 	if "Editorial" in str(line) and "href=\"/blog/entry" in str(line):
# 		print(line)

# def isEditorial(blogName):
# 	texts = ["Editorial", "Разбор"]
# 	return any(text in blogName for text in texts)




# for blogEntryId in range(87849, 88100):
# 	print(f"Current blog: {blogEntryId}")
# 	blog = requester.make_api_query(
# 		handler="blogEntry.view",
# 		params={"blogEntryId": blogEntryId}
# 	)

# 	print(blog)

# 	if blog["status"] == "OK" and isEditorial(blog["result"]["title"]):
# 		editorialIdsFile.write(f"{blogEntryId}\n")
# 		editorialIdsFile.flush()

# 	time.sleep(2.1)
