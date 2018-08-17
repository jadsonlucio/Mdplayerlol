import json
import pandas as pd
import numpy as np
from .. import constants

__all__=["set_champion_data", "set_normalized_attributes", "set_relative_attributes"]

def set_champion_data(matchs_dataframe):
    # carrega o json com as informações dos campeões
    with open(constants.champions_json_path, 'r') as file:
        file.seek(0)
        champion_json = json.load(file)

    champion_data = champion_json["data"].values()
    champions_info_data = []

    for champion_id in matchs_dataframe["championId"]:
        for champion in champion_data:
            if(int(champion["key"]) == int(champion_id)):
                champions_info_data.append(
                    [champion["name"], *champion["info"].values(), *champion["tags"]])

    champion_info_dataframe = pd.DataFrame(
        data=champions_info_data, columns=constants.champion_info)

    matchs_dataframe.update(champion_info_dataframe)

    return matchs_dataframe


def set_normalized_attributes(matchs_dataframe, attributes):
    for attribute in attributes:
        serie = matchs_dataframe.get(attribute)
        serie = (serie - min(serie)) / (max(serie) - min(serie))
        matchs_dataframe["norm_" + attribute] = serie

    return matchs_dataframe


def set_relative_attributes(match_dataframe, attributes , matchs_count=None):
    if matchs_count is not None:
        print("{0} {1}".format(matchs_count.value,matchs_count.max_matchs))
        matchs_count.value = matchs_count.value+1

    for attribute in attributes:
        array_time_1 = match_dataframe[attribute][:5]
        array_time_2 = match_dataframe[attribute][5:]
        soma_array_time_1 = sum(array_time_1)
        soma_array_time_2 = sum(array_time_2)
        if(soma_array_time_1 == 0):
            rel_array_time_1 = np.zeros(5)
        else:
            rel_array_time_1 = [
                value / soma_array_time_1 for value in array_time_1]

        if(soma_array_time_2 == 0):
            rel_array_time_2 = np.zeros(5)
        else:
            rel_array_time_2 = [
                value / soma_array_time_2 for value in array_time_2]

        array_match = []
        [array_match.append(value) for value in rel_array_time_1]
        [array_match.append(value) for value in rel_array_time_2]

        match_dataframe["rel_" + attribute] = np.array(array_match)

    return match_dataframe


