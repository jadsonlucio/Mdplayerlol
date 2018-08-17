from functions import Pre_processing
from functions import run_test

import pandas as pd

dataframe = pd.read_csv(
    r"C:\Users\pandaQ\Documents\Github\Mdplayerlol\datasets\ranked_dataset.csv")

pre_process = Pre_processing(dataframe)

dataframe = pre_process.pre_processe_matchs(time_limit_range=(1800, 3000))
routes_pipeline,routes_features_score,cross_validation_models=run_test(dataframe)


print(routes_pipeline["adc"])