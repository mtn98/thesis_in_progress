import pandas as pd
import glob
import re
from gensim.utils import simple_preprocess

PRESIDENCIES = {
    "Obama1": range(2009, 2013),
    "Obama2": range(2013, 2017),
    "Trump": range(2017, 2021)  # dataset ends in december 2019
}


# the bz2 files were downloaded from https://zenodo.org/records/5851729

def clean_reddit(text):
    text = re.sub(r'http\S+', '', text)  # remove URLs
    text = re.sub(r'\s+/[ru]/\S+', '', text)  # remove user/subreddit mentions
    text = re.sub(r'\&\w+;', '', text)  # remove HTML entities like &gt;
    text = re.sub(r'\*+', '', text)  # remove markdown asterisks
    return text


# state a file within which you saved the subreddits of interest - currently prodemocrat subreddits
# see info.py for how the txt file was created
subreddit_file = "DEM_subs.txt"
sub_orient = subreddit_file.removesuffix("_subs.txt")  # for naming output
with open(subreddit_file, 'r') as f:
    subreddits = set(f.read().strip().split('\n'))

# creates one txt file containing all comments generated within
# the DEM/REP/US (depending on subreddit_file) communities during each presidency
for pres, years in PRESIDENCIES.items():
    with open(f"comments_{pres}_{sub_orient}.txt", "w", encoding="utf-8") as output_file:
        for year in years:
            # selects only the files relevant for the given year
            bz2_files = sorted(glob.glob(f"politosphere_zip/comments_{year}*.bz2"))
            if not bz2_files:
                print(f"No files found for year {year}")
                break

            for file_path in bz2_files:  # loops over the relevant files
                print(file_path)
                comments = []
                for c in pd.read_json(file_path, compression='bz2', lines=True, dtype=False, chunksize=10000):
                    c = c[c.subreddit.isin(subreddits)]
                    comments.append(c["body"])

                comments = pd.concat(comments, sort=True)
                cleaned_comments = comments.apply(clean_reddit)
                preprocessed_comments = cleaned_comments.apply(lambda x: simple_preprocess(x, deacc=True))

                for comment in preprocessed_comments:
                    if comment:  # skip empty lists
                        output_file.write(" ".join(comment) + "\n")
