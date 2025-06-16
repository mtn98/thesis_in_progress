#This file creates json files containing the wordsets that will later be used for ML-EAT.
#Wordsets are created from both the full SADCAT dictionaries and the original seed dictionaries from Nicolas et al. (2021).
#The target wordsets denoting 'democrat' and 'republican' will be defined with careful consideration 
#(using politics_dict from SADCAT directly would include politically loaded terms too broad in meaning e.g. anarchist, fascist etc)

from pathlib import Path
import pandas as pd
import json

path = Path('dictionaries/SADCAT_dictionaries.csv')  #accessed from R package 'SADCAT' - SADCAT_dict.R
path1 = Path('dictionaries/BRM-emot-submit.csv') #downloaded at: https://link.springer.com/article/10.3758/s13428-012-0314-x#SecESM1

df = pd.read_csv(path)
df1 = pd.read_csv(path1)

#NB: within SADCAT_dictionaries.csv Agency = Assertiveness
of_interest_dict = ['Sociability','Morality', 'Ability', 'Assertiveness']

#adding valence to SADACT from BRM-emot
df['valence'] = df['values0'].map(df1.set_index('Word')['V.Mean.Sum']) 
#centering valence (so that negative values indicate negative valence)
df['valence']=df['valence']-5

summary_df = pd.DataFrame(columns= ["Dictionary", "entries", "high", "h_positive", "h_negative","h_valence_issues", "low", "l_positive", "l_negative", "l_valence_issues" ])
wordset = {  #This structure mirrors what has been done by Wolfe et al. (2024)
    'A' : [],   #attribute wordset (e.g. high agency) 
    'B' : [],   #attribute wordset (e.g. low agency)
    'X' : [],   #target worset ('democrats')
    'Y' : [],   #target wordset ('republicans')
    'eat_name': "", #given that target wordsets remain unchanged, wi ll benamed after the dimension under consideration (e.g. agency)
    'A_name' : "",  #
    'B_name' : "",  #
    'X_name' : "Democrats",  
    'Y_name' : "Republicans"
}

#
for dict_name in of_interest_dict:
    col_name = f"{dict_name}_dict"
    direction_col= f"{dict_name}_dir"
    valence_cols =[f'{col_name}_Pos',f'{col_name}_Neg']
    subset = df[df[col_name] ==1]
    of_interest_columns = ['values0', direction_col, 'val', 'valence']
    tot = len(subset)

    #saving csv of each dimension to later inspect  - remove '#' if desired
    #subset.to_csv(f'{dict_name}.csv')

    high = subset[subset[direction_col] == 1]
    low = subset[subset[direction_col] == -1]
    high_pos = high[(high[valence_cols[0]]==1) & (high['valence'] >= 0)]
    high_neg = high[(high[valence_cols[1]]==1) & (high['valence'] < 0)]
    low_pos = low[(low[valence_cols[0]]==1) & (low['valence'] >= 0)]
    low_neg = low[(low[valence_cols[1]]==1) & (low['valence'] < 0)]
    
    #simplest way to address valence issues: keeping only high_pos and low_neg
    wordset['A'] = high_pos['values0'].to_list()
    wordset['B'] =low_neg['values0'].tolist()
    wordset['eat_name'] = dict_name
    json_filename = f'dictionaries/{dict_name}_consistant_wordset.json'
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(wordset, f, ensure_ascii=False, indent= 2)


    n_high = len(high)
    n_low = len(low)
    n_high_pos = len(high_pos)
    n_high_neg = len(high_neg)
    n_high_issues = n_high-n_high_pos-n_high_neg
    n_low_pos = len(low_pos)
    n_low_neg = len(low_neg)
    n_low_issues = n_low-n_low_pos-n_low_neg

    summary_df.loc[len(summary_df)] = [dict_name, tot, n_high, n_high_pos, n_high_neg, n_high_issues, n_low, n_low_pos, n_low_neg, n_low_issues]
    

summary_df.to_csv('dictionaries/summary.csv')