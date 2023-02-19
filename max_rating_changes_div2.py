from lib import Requester
import re
from termcolor import colored
from collections import namedtuple

requester = Requester(max_rps=0.1)

contests = requester.make_api_query("contest.list", {})['result']
print(contests)

cnt = 0

UserNewRating = namedtuple('UserNewRating', ['handle', 'newRating', 'contest'])

max_new_ratings = []
LIMIT = 10000
MAX_TRIES = 10
flag = False

for contest in contests:
    if cnt == -1:
        break
    if not re.match('^.*Div\. ?2.*$', contest['name']) or re.match('^.*Div\. ?1.*$', contest['name']):
        print(f'Contest {contest["name"]} is not Div 2')
        continue
    tries = MAX_TRIES
    while tries > 0:
        tries -= 1
        try:
            print(colored(f"Requesting {contest['name']}", 'light_blue'))
            ratingChanges = requester.make_api_query("contest.ratingChanges", {"contestId": contest["id"]})
            if ratingChanges['status'] == 'FAILED':
                print(colored(f"{contest['name']} {ratingChanges['comment']}", 'red'))
            else:
                ratingChanges = ratingChanges['result']
                print(colored(str(len(ratingChanges)), 'green', attrs=['bold']))
                for ratingChange in ratingChanges:
                    max_new_ratings.append(UserNewRating(ratingChange['handle'], ratingChange['newRating'], contest['name']))
                max_new_ratings.sort(key=lambda x: x.newRating, reverse=True)
                if len(max_new_ratings) > LIMIT:
                    max_new_ratings = max_new_ratings[:LIMIT]
                cnt += 1
            break
        except:
            pass

best_file = open("best_ratings_after_div2.csv", "w")

for handle, newRating, contest in max_new_ratings:
    best_file.write(f'{newRating},{handle},{contest}\n')
    print(newRating, handle, contest)