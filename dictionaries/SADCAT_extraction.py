#This file creates json files containing the wordsets that will later be used for ML-EAT.
#Wordsets are created from both the full SADCAT dictionaries and the original seed dictionaries from Nicolas et al. (2021).
#The target wordsets denoting 'democrat' and 'republican' will be defined with careful consideration 
#(using politics_dict from SADCAT directly would include politically loaded terms too broad in meaning e.g. anarchist, fascist etc)

from pathlib import Path
import pandas as pd
import json
import copy


Path("SADCAT").mkdir(parents=True, exist_ok=True)
Path("seed").mkdir(parents=True, exist_ok=True)
path = Path('SADCAT_dictionaries.csv')  #accessed from R package 'SADCAT' - SADCAT_dict.R
path1 = Path('BRM-emot-submit.csv') #downloaded at: https://link.springer.com/article/10.3758/s13428-012-0314-x#SecESM1
path2 = Path('Seed_Dictionaries.csv') #downloaded from https://osf.io/yx45f/files/osfstorage
df = pd.read_csv(path)
df1 = pd.read_csv(path1)
df2= pd.read_csv(path2)

#NB: within SADCAT_dictionaries.csv Assertiveness, in Seed_dictionaries_csv 'Agency'
of_interest_dict = ['Sociability','Morality', 'Ability', 'Assertiveness']

#adding valence to SADACT and Seed dictionaries from BRM-emot
df['valence'] = df['values0'].map(df1.set_index('Word')['V.Mean.Sum'])
df2['valence'] = df2['term'].map(df1.set_index('Word')['V.Mean.Sum']) 
#centering valence (so that negative values indicate negative valence)
df['valence']=df['valence']-5
df2['valence']=df2['valence']-5



summary_df = pd.DataFrame(columns= ["Dictionary", "entries", "high", "h_positive", "h_negative","h_valence_issues", "low", "l_positive", "l_negative", "l_valence_issues" ])
template_wordset = {  #This structure mirrors what has been done by Wolfe et al. (2024)
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

for dict_name in of_interest_dict:

    seed_wordset = copy.deepcopy(template_wordset)
    SADCAT_wordset = copy.deepcopy(template_wordset)

    #seed dictionaries 
    if dict_name == 'Assertiveness':
        dimension = df2[df2['Dictionary'] == 'Agency']
        low_s = df2[(df2['Dictionary'] == 'Agency') & (df2['Dir']=='low')].drop_duplicates(subset='term')
        high_s = df2[(df2['Dictionary'] == 'Agency') & (df2['Dir']=='high')].drop_duplicates(subset='term')
    else:   
        dimension =  df2[df2['Dictionary'] == dict_name]
        low_s = df2[(df2['Dictionary'] == dict_name) & (df2['Dir']=='low')].drop_duplicates(subset='term')
        high_s = df2[(df2['Dictionary'] ==  dict_name) & (df2['Dir']=='high')].drop_duplicates(subset='term')
    
    dimension = dimension.copy()
    dimension['Dir'] = dimension['Dir'].replace({'high': 1, 'low': -1}).astype(int)

    #saving csv of each dimension to later inspect  - remove '#' if desired
    #dimension = dimension.copy()
    #dimension['Dir'] = dimension['Dir'].replace({'high': 1, 'low': -1}).astype(int)
    #dimension[['term','valence','Dir']].to_csv(f'seed/seed_{dict_name}.csv', index=False)

    seed_wordset['A'] = high_s['term'].to_list()
    seed_wordset['A_name'] = f'high {dict_name}'
    seed_wordset['B'] =low_s['term'].tolist()
    seed_wordset['B_name'] = f'low {dict_name}'
    seed_wordset['eat_name'] = f'seed {dict_name}'
    json_seed = f'{dict_name}_seed_wordset.json'
    with open(json_seed, "w", encoding="utf-8") as f:
        json.dump(seed_wordset, f, ensure_ascii=False, indent= 2)

    #SADCAT dictionaries
    col_name = f"{dict_name}_dict"
    direction_col= f"{dict_name}_dir"
    valence_cols =[f'{col_name}_Pos',f'{col_name}_Neg']
    
    of_interest_columns = ['values0', direction_col, 'Val', 'valence', f'{col_name}_Pos',f'{col_name}_Neg']
    subset = df[df[col_name] ==1]
    tot = len(subset)
    #saving csv of each dimension to later inspect  - remove '#' if desired
    #subset[of_interest_columns].to_csv(f'SADCAT/{dict_name}.csv', index=False)

    high = subset[subset[direction_col] == 1]
    low = subset[subset[direction_col] == -1]
    high_pos = high[(high[valence_cols[0]]==1) & (high['valence'] >= 0)]
    high_neg = high[(high[valence_cols[1]]==1) & (high['valence'] < 0)]
    low_pos = low[(low[valence_cols[0]]==1) & (low['valence'] >= 0)]
    low_neg = low[(low[valence_cols[1]]==1) & (low['valence'] < 0)]
    
    #simplest way to address valence issues: keeping only high_pos and low_neg
    SADCAT_wordset['A'] = high_pos['values0'].to_list()
    SADCAT_wordset['A_name'] = f'high-positive {dict_name}'
    SADCAT_wordset['B'] =low_neg['values0'].tolist()
    SADCAT_wordset['B_name'] = f'low-negarive {dict_name}'
    SADCAT_wordset['eat_name'] = dict_name

    json_SADCAT = f'{dict_name}_consistant_wordset.json'
    with open(json_SADCAT, "w", encoding="utf-8") as f:
        json.dump(SADCAT_wordset, f, ensure_ascii=False, indent= 2)


    n_high = len(high)
    n_low = len(low)
    n_high_pos = len(high_pos)
    n_high_neg = len(high_neg)
    n_high_issues = n_high-n_high_pos-n_high_neg
    n_low_pos = len(low_pos)
    n_low_neg = len(low_neg)
    n_low_issues = n_low-n_low_pos-n_low_neg

    summary_df.loc[len(summary_df)] = [dict_name, tot, n_high, n_high_pos, n_high_neg, n_high_issues, n_low, n_low_pos, n_low_neg, n_low_issues]

summary_df.to_csv('summary.csv')   



