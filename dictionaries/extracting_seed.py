#script da ripulire
from pathlib import Path
import pandas as pd
import json

#'Seed_Dictionaries.csv' was downloaded from https://osf.io/yx45f/files/osfstorage
path = Path('Seed_Dictionaries.csv')

df = pd.read_csv(path)
of_interest_dict = ['Sociability','Morality', 'Ability', 'Agency']
#warmth =['Sociability', 'Morality']
#competence = ['Ability', 'Agency']


infos = []
for dict_name in of_interest_dict:
    low = df[(df['Dictionary'] == dict_name) & (df['Dir']=='low')].drop_duplicates(subset='term')
    high = df[(df['Dictionary'] == dict_name) & (df['Dir']=='high')].drop_duplicates(subset='term')
    infos.append(
        f'{dict_name}:\n'
        f'\t\t-high:{len(high)}\n'
        f'\t\t-low:{len(low)}\n'
    )
    file_low = f'{dict_name}_seed_low.txt'
    file_high= f'{dict_name}_seed_high.txt'
    low['term'].to_csv(file_low, header= False, index= False)
    high['term'].to_csv(file_high, header= False, index= False)

with open("seed_dict_summary.txt", "w") as f:
    f.write("\n".join(infos))  