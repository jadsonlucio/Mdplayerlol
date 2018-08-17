from functions import Pre_processing
from functions import run_test

import pandas as pd

array_dataframe = [pd.read_csv(r"C:\Users\Jadson\Documents\GitHub\Mdplayerlol\datasets\dataframe_{0}.csv".format(cont)) for cont in range(0,8)]
dataframe = pd.concat(array_dataframe)
dataframe['win'] = dataframe['win'].map({'Fail': 0, 'Win': 1})

obj_pre_process = Pre_processing(dataframe)

dataframe = obj_pre_process.pre_processe_matchs(time_limit_range=(1800, 3000))
routes_pipeline,routes_features_score,cross_validation_models=run_test(dataframe)


print(routes_features_score)
print(cross_validation_models)