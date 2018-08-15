import pandas as pd
from . import constants


def set_position(dicionario: dict) -> object:
    """
    :param dicionario: Dicionario das linhas de um dataframe.
    :return:
    """
    if dicionario["role"] == "DUO_CARRY":
        return "adc"
    elif dicionario["role"] == "DUO_SUPPORT":
        return "sup"
    elif dicionario["lane"] == "MIDDLE":
        return "mid"
    elif dicionario["lane"] == "JUNGLE":
        return "jg"
    elif dicionario["lane"] == "TOP":
        return "top"
    else:
        return None


def validate_match(match_dataframe):
    """
    verifica se uma partida é valida ou não, caso seja valida retorna
    a partida organizada de acorodo com as posições.

    Uma partida é valida se a quantidade de jogadores for 10
    e se cada jogador do time foi identificado de acordo com a sua posição.

    :param match_dataframe: dataframe de partidas.
    """
    if len(match_dataframe) == 10:
        team_1, team_2 = match_dataframe[:5], match_dataframe[5:10]

        team_1 = team_1.sort_values("position")
        team_2 = team_2.sort_values("position")

        for team_1_pos, team_2_pos, position in zip(team_1["position"], team_2["position"],
                                                    constants.lanes_positions):

            if team_1_pos != team_2_pos or team_1_pos != position:
                return None

        match_dataframe = pd.concat([team_1, team_2])
        return match_dataframe

    else:
        return None


def filter_valid_matchs(matchs_dataframe: pd.DataFrame) -> None:
    """
    Filtra somente as partidas validas, que tem 10 jogadores e que cada jogador
    do time foi identificado de acordo com a sua posição

    :param matchs_dataframe: Dataframe de partida.
    """
    if "position" not in matchs_dataframe.columns:
        serie = matchs_dataframe.apply(set_position, axis=1)
        matchs_dataframe.insert(loc=0, column="position", value=serie)

    matchs_dataframe = matchs_dataframe[matchs_dataframe.position!=None]

    matchs_dataframes = []

    for label, match_dataframe in matchs_dataframe.groupby("gameCreation"):
        match_dataframe = validate_match(match_dataframe)

        if match_dataframe is not None:
            matchs_dataframes.append(match_dataframe)

    matchs_dataframe = pd.concat(matchs_dataframes)

    return matchs_dataframe

def filter_matchs_by_atributes(matchs_dataframe, time_limit_range, queue_id):
    if isinstance(time_limit_range, tuple):
        time_limit_range = list(time_limit_range)

    if isinstance(time_limit_range, list):
        if time_limit_range[0] is None:
            time_limit_range[0] = 0
        if time_limit_range[1] is None:
            time_limit_range[1] = max(matchs_dataframe["gameDuration"])

        min_time = time_limit_range[0]
        max_time = time_limit_range[1]
        gameDuration = matchs_dataframe["gameDuration"]
        queueId = matchs_dataframe["queueId"]

        matchs_dataframe = matchs_dataframe[(gameDuration > min_time) & (
                gameDuration < max_time) & (queueId == queue_id)]


        return matchs_dataframe

