from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

__all__ = ["get_features_importance", "feature_importance_by_model", "pipeline"]

def get_features_importance(model):
    feature_importances_attributes = ["feature_importances_"]
    for feature_importances_attribute in feature_importances_attributes:
        try:
            feature_importances = model.__getattribute__(feature_importances_attribute)
            return feature_importances
        except Exception:
            pass
    else:
        raise AttributeError("model of type {0} has no attributes {1} to compute features "
                             "importance".format(type(model).__name__, tuple(feature_importances_attributes)))

def feature_importance_by_model(dataframe, model, trainX_attributes, trainY_attributes):
    trainX_dataframe = dataframe.get(trainX_attributes)
    trainY_dataframe = dataframe.get(trainY_attributes)

    model.fit(trainX_dataframe, trainY_dataframe)

    return {feature_name: feature_importance for feature_name, feature_importance in
                    zip(trainX_attributes, get_features_importance(model))}

def pipeline(x, y, train_size,model_feature_selection, model_test, model_type):
    trainX,testX,trainY,testY = train_test_split(x, y, train_size=train_size, test_size=1-train_size,
                                                                                    random_state=4)
    _pipeline=Pipeline([("feature_selection",SelectFromModel(model_feature_selection)),(model_type,model_test)])
    _pipeline.fit(trainX, trainY)
    accuracy = f1_score(testY, _pipeline.predict(testX))
    threshold_ = _pipeline.named_steps["feature_selection"].threshold_
    features_importance = get_features_importance(_pipeline.named_steps["feature_selection"].estimator_)
    features_selecteds = [(count,importance) for count,importance in enumerate(features_importance) if importance>threshold_]
    
    model_selection_name = model_feature_selection.__class__.__name__
    model_test_name = model_test.__class__.__name__
    return {"train_size":len(trainX),
           "test_size":len(testX),
           "accuracy":accuracy,
           "features_selected":features_selecteds,
           "model_selection": model_selection_name,
           "model_test": model_test_name 
           }