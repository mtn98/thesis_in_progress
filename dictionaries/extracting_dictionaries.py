#script da ripulire
from pathlib import Path
import pandas as pd
import json

#'Full_Dictionaries.csv' was downloaded from: https://osf.io/yx45f/files/osfstorage

path = Path('Full_Dictionaries.csv')
df = pd.read_csv(path)
of_interest_dict = ['Sociability','Morality', 'Ability', 'Agency']

#nice_extras = ['Politics', 'insults', 'social_groups']

word_columns = [
    'original word',
    'preprocessed word 2 (no spaces)',
    'preprocessed word 3 (lemmatized)',
    'preprocessed word 4 (minus one trailing s)'
]

#currently saves txt files for each dictionaryXdirection, will be changed to saving 
#one json file, with a (python) dictionary structure like:
#   dimension: {
#               high: []
#               low: []}
#   dimension: {
#               high: []
#               low: []}
#this will be done after resolving the valence issues and most likely by only considering SADCAT_dictionaries.csv, i.e. Full_Diictionaries.csv won't be used
for dict_name in of_interest_dict:
    col_name = f"{dict_name} dictionary" 
    dir_col = f"{dict_name} direction"
    relevant_rows = df[df[col_name] == 1]

    for direction in [-1,1]:
        #selects only the rows containing words belonging to the current dictionary of interest
        subset = relevant_rows[relevant_rows[dir_col]== direction] 

        txt_filename = f"{dict_name.lower()}_{direction}.txt"
        subset["original word"].to_csv(txt_filename, index= False, header=False)
        print(f"saved {txt_filename} with {len(subset)} entries")

        #csv_filename = f"{dict_name.lower()}_{direction}.csv"
        #subset[word_columns].to_csv(csv_filename, index= False)
        #print(f"Saved structured CSV: {csv_filename}")

        #json_filename =  f"{dict_name.lower()}_{direction}.json"
        #records = subset[word_columns].to_dict(orient="records")
        #with open(json_filename, "w", encoding="utf-8") as f:
        #    json.dump(records, f, ensure_ascii=False, indent= 2)
        #print(f"Saved structured JSON: {json_filename}")
