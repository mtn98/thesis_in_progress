from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from scipy.stats import pearsonr, spearmanr


of_interest_dict = ['Sociability','Morality', 'Ability', 'Assertiveness']
plot_dir = Path("valence_plots")
plot_dir.mkdir(exist_ok=True)



def compute_sad_val(row, pos_col, neg_col):
    if row[pos_col] ==1 and row[neg_col] == 0:
        return 1
    if row[pos_col] ==0 and row[neg_col] == 1:
        return -1
    else:
        return 0 

def plot_dimension(dictionary, plot_dir):
    
    path1 = Path(f'SADCAT/{dictionary}.csv')
    path2 = Path(f'seed/seed_{dictionary}.csv')
    SADCAT_df = pd.read_csv(path1)
    seed_df = pd.read_csv(path2)

    #remove missing values
    SADCAT_df=SADCAT_df[SADCAT_df['valence'].notna()]
    SADCAT_df=SADCAT_df[(SADCAT_df[f'{dictionary}_dir'] == -1) | (SADCAT_df[f'{dictionary}_dir'] == 1)]
    seed_df=seed_df[seed_df['valence'].notna()]

    #SADCAT currently stores valence as 2 dichotomous variables: Dimension_dict_Pos & Dimension_dict_Neg
    #to color code later i need to translate into a single variable for ease
    pos_col, neg_col = f'{dictionary}_dict_Pos', f'{dictionary}_dict_Neg' 
    SADCAT_df['sad_val'] = SADCAT_df.apply(lambda row: compute_sad_val(row, pos_col, neg_col), axis =1)
    
    #plotting: 
    #Define a custom color map
    color_map = { -1: 'red', 0 : 'gray', 1: 'green' }  # You can adjust colors as you like
    fig, (seed, SADCAT, vals_corr) = plt.subplots(1,3, figsize = (15, 5), gridspec_kw={'width_ratios': [0.9, 0.9, 2.2]})
    plt.subplots_adjust(wspace=1)
    x_jittered = seed_df['Dir'] + np.random.normal(0, 0.03, size=len(seed_df))
    seed.scatter(x_jittered, seed_df['valence'], s = 20)
    seed.set_title(f'Seed {dictionary}')
    seed.set_ylabel('BRM-emot Valence', fontsize=16)
    seed.set_xlabel('Direction', fontsize=16)
    seed.set_xticks([-1,1])
    seed.axhline(y=0, color='gray', linestyle='--', linewidth=1.5)

    colors = SADCAT_df['sad_val'].map(color_map)
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Negative', markerfacecolor='red', markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Neutral/Missing', markerfacecolor='gray', markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Positive', markerfacecolor='green', markersize=8),]
    
    x_jittered = SADCAT_df[f'{dictionary}_dir'] + np.random.normal(0, 0.03, size=len(SADCAT_df))
    SADCAT.scatter(x_jittered, SADCAT_df['valence'], c=colors, s = 20)
    grouped = [SADCAT_df.loc[SADCAT_df[f'{dictionary}_dir'] == d, 'valence'] for d in [-1, 1]]
    SADCAT.violinplot(grouped, positions=[-1, 1])
    SADCAT.scatter(x_jittered, SADCAT_df['valence'], c=colors, s = 20)
    SADCAT.set_title(f'Full {dictionary}')
    SADCAT.set_ylabel('BRM-emot Valence', fontsize=16)
    SADCAT.set_xlabel('Direction', fontsize=16)
    SADCAT.set_xticks([-1,1])
    SADCAT.axhline(y=0, color='gray', linestyle='--', linewidth=1.5)
    SADCAT.legend(
        handles=legend_elements,
        title="SADCAT Valence",
        loc='center left',
        bbox_to_anchor=(1.05, 0.5),
        fontsize='small',
        title_fontsize='small'
    )

    valid_df = SADCAT_df[['valence', 'Val']].dropna()
    pearson_r, pearson_p = pearsonr(valid_df['valence'], valid_df['Val'])
    spearman_rho, spearman_p = spearmanr(valid_df['valence'], valid_df['Val'])
    vals_corr.scatter(SADCAT_df['valence'], SADCAT_df['Val'], s = 10)
    #regression line
    coeffs = np.polyfit(valid_df['valence'], valid_df['Val'], 1)
    regression_line = np.poly1d(coeffs)
    x_vals = np.linspace(valid_df['valence'].min(), valid_df['valence'].max(), 100)
    vals_corr.plot(x_vals, regression_line(x_vals), color='black', linestyle='--', linewidth=1)
    vals_corr.text(0.05, 0.95,
                   f"$r$ = {pearson_r:.2f}",
                   transform=vals_corr.transAxes,
                   fontsize=10,
                   verticalalignment='top')
    vals_corr.set_ylabel('SADCAT val', fontsize=16)
    vals_corr.set_xlabel('BRM-emot Valence', fontsize=16)


    plt.savefig(plot_dir/f'{dictionary}.png', bbox_inches = 'tight')


for dict in of_interest_dict:
    plot_dimension(dict, plot_dir)