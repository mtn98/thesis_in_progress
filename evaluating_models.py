import pandas as pd
import numpy as np
import glob
import json
from gensim.models import KeyedVectors
from scipy.stats import spearmanr

#downloaded the MEN folder from  https://staff.fnwi.uva.nl/e.bruni/MEN

df = pd.read_csv("MEN/MEN_dataset_natural_form_full", sep=" ", header=None)
df.columns = ["word1", "word2", "similarity"]
word_pairs_eval = {}

#I have saved my models within Presidency_ORIENTATION_400D folders, e.g. Obama1_DEM_400D
models = sorted(glob.glob('*400D'))

def get_similarity(row, vectors):
    w1, w2 = row['word1'], row['word2']
    if w1 in vectors and w2 in vectors:
        return vectors.similarity(w1, w2)
    else:
        return np.nan

for model in models:
    vectors = KeyedVectors.load_word2vec_format(f"{model}/vectors.txt", binary=False)
    #evaluating in reference to the whole MEN dataset
    pearson, spearman, oov_ratio = vectors.evaluate_word_pairs("MEN/MEN_dataset_natural_form_full", delimiter = ' ')
    word_pairs_eval[model] = {
        'pearson': pearson, 
        'spearman': spearman,
        'oov_ratio' :oov_ratio
        }
    #working toward the evaluation based on a shared subset
    df[model] = df.apply(lambda row: get_similarity(row, vectors), axis=1)
   
subset_df = df.dropna(subset= models)

subset_df.to_csv("MEN_common_subset.csv", index=False)


for model in models:
    rho, pval = spearmanr(subset_df['similarity'], subset_df[model])
    word_pairs_eval[model]['subset evaluation'] = {
        'rho': rho,
        'p': pval
    }
word_pairs_eval['number of common pairs'] = len(subset_df)

with open("word_pairs_eval.json", "w") as f:
    json.dump(word_pairs_eval, f, indent=4, default=str)