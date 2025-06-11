#this file identifies the reddit communities that are of interest and stores them 
#in a txt file for later use - see extract_preprocess.py

import json

#'subreddits_metadata.json' was downloaded from: https://zenodo.org/records/5851729

with open('subreddits_metadata.json', 'r') as file:
    us_entries = []
    dem_entries= []
    rep_entries= []
    for line in file:
        # Load each line as a separate JSON object
        entry = json.loads(line)
        #within the dataset, '' stands for us, while 'us' specifically denotes 
        #subreddits dedicated to (us) state-level politics (e.g. MissouriPolitics )
        if  entry.get("region") == "us" or entry.get("region") == "": 
            if entry.get("party") == "dem":
                dem_entries.append(entry)
            elif entry.get("party") == "rep":
                rep_entries.append(entry)
            
            us_entries.append(entry)

print(f"{len(dem_entries)}, {len(rep_entries)}, {len(us_entries)}")

#US SUB LIST TXT
from pathlib import Path
path_us = Path('US_subs.txt')
us_subs = [f"{us_sub['subreddit']}\n" for us_sub in us_entries]
with path_us.open("w") as file:
    file.writelines(us_subs)

#all dem entries
path_dem = Path('DEM_subs.txt')
dem_subs = [f"{dem_sub['subreddit']}\n" for dem_sub in dem_entries]
with path_dem.open("w") as file:
    file.writelines(dem_subs)
#all rep entries 
path_rep = Path('REP_subs.txt')
rep_subs = [f"{rep_sub['subreddit']}\n" for rep_sub in rep_entries]
with path_rep.open("w") as file:
    file.writelines(rep_subs)


#the following code considers banned and non-banned us subreddits separately 
#(no pro-dem banned subreddits are present)

#us entries no ban and ban
path_NB_us = Path('NB_US_subs.txt')
path_BAN_us = Path('Banned_US_subs.txt')
NB_us_subs = [f"{us_sub['subreddit']}\n" for us_sub in us_entries if us_sub.get('banned') == 0]
BAN_us_subs = [f"{us_sub['subreddit']}\n" for us_sub in us_entries if us_sub.get('banned') == 1]
with path_NB_us.open("w") as file:
    file.writelines(NB_us_subs)
with path_BAN_us.open("w") as file:
    file.writelines(BAN_us_subs)

#dem entries no ban and ban 
path_NB_dem = Path('NB_dem_subs.txt')
path_BAN_dem = Path('Banned_dem_subs.txt')
NB_dem_subs = [f"{dem_sub['subreddit']}\n" for dem_sub in dem_entries if dem_sub.get('banned') == 0]
BAN_dem_subs = [f"{dem_sub['subreddit']}\n" for dem_sub in dem_entries if dem_sub.get('banned') == 1]
with path_NB_dem.open("w") as file:
    file.writelines(NB_dem_subs)
with path_BAN_dem.open("w") as file:
    file.writelines(BAN_dem_subs)

#rep entries no ban and ban
path_NB_rep = Path('NB_rep_subs.txt')
path_BAN_rep = Path('Banned_rep_subs.txt')
NB_rep_subs = [f"{rep_sub['subreddit']}\n" for rep_sub in rep_entries if rep_sub.get('banned') == 0]
BAN_rep_subs = [f"{rep_sub['subreddit']}\n" for rep_sub in rep_entries if rep_sub.get('banned') == 1]
with path_NB_rep.open("w") as file:
    file.writelines(NB_rep_subs)
with path_BAN_rep.open("w") as file:
    file.writelines(BAN_rep_subs)