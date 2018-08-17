import pandas as pd

from sklearn.ensemble import *
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from .model_selection import pipeline
from .. import constants

__all__ = ["calculate_score","run_test"]

STANDARD_MODELS = {
    "ExtraTreesClassifier": ExtraTreesClassifier,
    "ExtraTreesRegressor": ExtraTreesRegressor,
    "RandomForestClassifier": RandomForestClassifier,
    "RandomForestRegressor": RandomForestRegressor
}

def calculate_score(matchs_dataframe, routes_attributes_score):
    def calculate_score(dict):
        score = 0
        route_scores = routes_attributes_score[dict["position"]]
        for attribute_name, attribute_score in route_scores.items():
            score = score+dict[attribute_name]*attribute_score

        return score

    serie = matchs_dataframe.apply(calculate_score, axis=1)
    matchs_dataframe.insert(loc=0, column="score", value=serie)

    return matchs_dataframe

def matchs_train_test_split(matchs_dataframe,train_size, test_size=None):
    if(test_size==None):
        test_size = 1-train_size
    matchs_dataframes = [dataframe for label,dataframe in matchs_dataframe.groupby("gameCreation")]
    train_dataframes, test_dataframes = train_test_split(matchs_dataframes, train_size=train_size,
                                                                             test_size=test_size)
    
    train_dataframe = pd.concat(train_dataframes) 
    test_dataframe = pd.concat(test_dataframes)

    return train_dataframe,test_dataframe

DEFAULT_TEST_PARMS={
    "pipeline_model_type": "classification",
    "pipeline_feature_selection_model": STANDARD_MODELS["RandomForestClassifier"](),
    "pipeline_test_mode": STANDARD_MODELS["RandomForestClassifier"](),
    "pipeline_input_attributes": constants.selected_attributes,
    "pipeline_output_attributes": "win",
    "pipeline_train_size": 0.75,
    "validation_size": 0.25,
    "cross_validation_models": [MLPClassifier(),RandomForestClassifier(),KNeighborsClassifier()]
}

def run_pipeline(train_matchs_dataframe, test_parms):
    routes_dataframe = [dataframe for label,dataframe in train_matchs_dataframe.groupby("position")]
    routes_pipeline = {}
    routes_features_score = {}
    for route_label,route_dataframe in zip(constants.lanes_positions,routes_dataframe):
        x = route_dataframe[test_parms["pipeline_input_attributes"]]
        y = route_dataframe[test_parms["pipeline_output_attributes"]]

        routes_pipeline[route_label] = pipeline(x, y, test_parms["pipeline_train_size"], 
        test_parms["pipeline_feature_selection_model"], test_parms["pipeline_test_mode"], 
        test_parms["pipeline_model_type"])

        routes_features_score[route_label] = {}
        for feature_index, feature_score in routes_pipeline[route_label]["features_selected"]:
            feature_name = test_parms["pipeline_input_attributes"][feature_index]
            routes_features_score[route_label][feature_name] = feature_score

    return routes_pipeline,routes_features_score

def run_validation(validation_matchs_dataframe, test_parms):
  
    x, y = [],[]
    for label,dataframe in validation_matchs_dataframe.groupby("gameCreation"):
        x.append(dataframe["score"])
        y.append(list(dataframe["win"])[0])

    cross_validation_models = {}
    for cross_validation_model in test_parms["cross_validation_models"]:
        model_name = cross_validation_model.__class__.__name__
        scores = cross_val_score(cross_validation_model, x, y, cv=5)
        mean = scores.mean()
        std = scores.std()
        cross_validation_models[model_name]=(mean,std)
    
    return cross_validation_models
    



def run_test(matchs_dataframe, test_parms=DEFAULT_TEST_PARMS):
    train_dataframe, validation_dataframe = matchs_train_test_split(matchs_dataframe,test_parms["pipeline_train_size"])
    routes_pipeline,routes_features_score = run_pipeline(train_dataframe, test_parms)
    validation_dataframe = calculate_score(validation_dataframe, routes_features_score)
    cross_validation_models=run_validation(validation_dataframe, test_parms)

    return routes_pipeline,routes_features_score,cross_validation_models



