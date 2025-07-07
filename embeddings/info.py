# this file identifies the reddit communities that are of interest and stores them
# in a txt file for later use - see extract_preprocess.py

import json
import requests
from pathlib import Path

if __name__ == "__main__":
    # 'subreddits_metadata.json' was downloaded from: https://zenodo.org/records/5851729
    response = requests.get('https://zenodo.org/records/5851729/files/subreddits_metadata.json?download=1')
    with open('subreddits_metadata.json', 'wb') as f:
        f.write(response.content)

    with open('subreddits_metadata.json', 'r') as file:
        us_entries = []
        dem_entries = []
        rep_entries = []
        for line in file:
            # Load each line as a separate JSON object
            entry = json.loads(line)
            # within the dataset, '' stands for us, while 'us' specifically denotes
            # subreddits dedicated to (us) state-level politics (e.g. MissouriPolitics )
            if entry.get("region") in ("us", ""):
                if entry.get("party") == "dem":
                    dem_entries.append(entry)
                elif entry.get("party") == "rep":
                    rep_entries.append(entry)
                else:
                    us_entries.append(entry)

    print(f"Democratic Entries: {len(dem_entries)} \n"
          f"Repubblican Entries {len(rep_entries)}, \n"
          f"USA Entries: {len(us_entries)}")

    with Path('US_subs.txt').open("w") as file:
        us_subs = [f"{us_sub['subreddit']}\n" for us_sub in us_entries]
        file.writelines(us_subs)

    # all dem entries
    with Path('DEM_subs.txt').open("w") as file:
        dem_subs = [f"{dem_sub['subreddit']}\n" for dem_sub in dem_entries]
        file.writelines(dem_subs)

    # all rep entries
    with Path('REP_subs.txt').open("w") as file:
        rep_subs = [f"{rep_sub['subreddit']}\n" for rep_sub in rep_entries]
        file.writelines(rep_subs)

    with Path('Banned_US_subs.txt').open("w") as file:
        BAN_us_subs = [f"{us_sub['subreddit']}\n" for us_sub in us_entries if us_sub.get('banned') == 1]
        file.writelines(BAN_us_subs)

    with Path('Banned_dem_subs.txt').open("w") as file:
        BAN_dem_subs = [f"{dem_sub['subreddit']}\n" for dem_sub in dem_entries if dem_sub.get('banned') == 1]
        file.writelines(BAN_dem_subs)

    with Path('Banned_rep_subs.txt').open("w") as file:
        BAN_rep_subs = [f"{rep_sub['subreddit']}\n" for rep_sub in rep_entries if rep_sub.get('banned') == 1]
        file.writelines(BAN_rep_subs)

    # dem entries no ban and ban
    with Path('NB_dem_subs.txt').open("w") as file:
        NB_dem_subs = [f"{dem_sub['subreddit']}\n" for dem_sub in dem_entries if dem_sub.get('banned') == 0]
        file.writelines(NB_dem_subs)

    # us entries no ban and ban
    with Path('NB_US_subs.txt').open("w") as file:
        NB_us_subs = [f"{us_sub['subreddit']}\n" for us_sub in us_entries if us_sub.get('banned') == 0]
        file.writelines(NB_us_subs)

    # rep entries no ban and ban
    with Path('NB_rep_subs.txt').open("w") as file:
        NB_rep_subs = [f"{rep_sub['subreddit']}\n" for rep_sub in rep_entries if rep_sub.get('banned') == 0]
        file.writelines(NB_rep_subs)
