from pathlib import Path
import pandas as pd

path = Path('SADCAT_dictionaries.csv')  #accessed from R package 'SADCAT' - SADCAT_dict.R
path1 = Path('BRM-emot-submit.csv') #downloaded at: https://link.springer.com/article/10.3758/s13428-012-0314-x#SecESM1

df = pd.read_csv(path)
df1 = pd.read_csv(path1)

#NB: within SADCAT_dictionaries.csv Agency = Assertiveness
of_interest_dict = ['Sociability','Morality', 'Ability', 'Assertiveness']

#adding valence to SADACT from BRM-emot
df['valence'] = df['values0'].map(df1.set_index('Word')['V.Mean.Sum']) 
#centering valence (so that negative values indicate negative valence)
df['valence']=df['valence']-5

infos = []
#EXPORTING CSV FILES for later use + storing some infos :

#currently saves csv files for each dictionaryXdirection, will be changed to saving 
#one json file, with a (python) dictionary structure like:
#   dimension: {
#               high: []
#               low: []}
#   dimension: {
#               high: []
#               low: []}
#this will be done after resolving the valence issues

for dict_name in of_interest_dict:
    col_name = f"{dict_name}_dict"
    dir_cols = {                    
        f"{col_name}_lo": 'low', 
        f"{col_name}_hi": 'high'}
    valence_cols =[f'{col_name}_Pos',f'{col_name}_Neg']
    relevant_rows = df[df[col_name] == 1]
    infos.append(f'{dict_name.upper()} dictionary:\n'
                 f'{len(relevant_rows)} entries, of which:')
    of_interest_columns = ['values0', 'Val', 'valence', f'{col_name}_Pos',f'{col_name}_Neg']
    

    for direction, text in dir_cols.items(): 
        subset = relevant_rows[relevant_rows[direction]== 1]
        positive = subset[(subset[valence_cols[0]] ==1) & (subset['valence']>0)]
        negative =  subset[(subset[valence_cols[1]] ==1) & (subset['valence']<0)]
        infos.append(f'{len(subset)} {text} direciton,\n'
                    f'{len(positive)} positive, {len(negative)} negative, {len(subset)-len(positive)-len(negative)} with valence issues')
        
        csv_filename = f"{dict_name.lower()}_{text}_SADCAT.csv" 
        subset[of_interest_columns].to_csv(csv_filename, index= False) 
        print(f"Saved structured CSV: {csv_filename}")

with open("SADCAT_valence.txt", "w") as f:
    f.write("\n".join(infos)) 