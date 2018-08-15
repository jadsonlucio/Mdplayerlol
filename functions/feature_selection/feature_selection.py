from sklearn.ensemble import *

STANDARD_MODELS = {
    "ExtraTreesClassifier": ExtraTreesClassifier,
    "ExtraTreesRegressor": ExtraTreesRegressor,
    "RandomForestClassifier": RandomForestClassifier,
    "RandomForestRegressor": RandomForestRegressor
}


def feature_importance_by_model(dataframe, model, trainX_attributes, trainY_attributes):
    trainX_dataframe = dataframe.get(trainX_attributes)
    trainY_dataframe = dataframe.get(trainY_attributes)

    model.fit(trainX_dataframe, trainY_dataframe)

    feature_importances_attributes = ["feature_importances_"]

    for feature_importances_attribute in feature_importances_attributes:
        try:
            feature_importances = model.__getattribute__(feature_importances_attribute)
            return {feature_name: feature_importance for feature_name, feature_importance in
                    zip(trainX_attributes, feature_importances)}
        except Exception:
            pass

    else:
        raise AttributeError("model of type {0} has no attributes {1} to compute features "
                             "importance".format(type(model).__name__, tuple(feature_importances_attributes)))


def calculate_score(dataframe, attributes_scores: dict):
    def calculate_score(dict):
        global attributes_scores
        score = 0
        for attribute_name, attribute_score in attributes_scores.items():
            score = score+dict[attribute_name]*attribute_score

        return score

    serie = dataframe.apply(calculate_score, axis=1)
    dataframe.insert(loc=0, column="score", value=serie)

    return dataframe