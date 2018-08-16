from pre_processing.pre_processing import Pre_processing
from feature_selection.feature_selection import feature_importance_by_model

from pre_processing import constants

from sklearn.ensemble import ExtraTreesClassifier

import pandas as pd

dataframe = pd.read_csv(
    r"/home/jadson/Documentos/Github/Mdplayerlol/datasets/ranked_dataset.csv")

pre_process = Pre_processing(dataframe)

dataframe = pre_process.pre_processe_matchs(time_limit_range=(1800, 3000))

result=pre_process.split_matchs_by_attribute("position")

selected_features=feature_importance_by_model(result[0], ExtraTreesClassifier(), constants.selected_attributes, "win")

print(selected_features)
