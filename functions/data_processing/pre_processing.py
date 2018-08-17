import pandas as pd

from . import feature_extraction
from . import matchs_selection
from .. import constants

class Match_process_count():
    def __init__(self,max_matchs):
        self.max_matchs=max_matchs
        self.value=0

class Pre_processing:
    def __init__(self, matchs_dataframe):
        self._matchs_dataframe = None
        self._matchs_dataframes = None

        self.matchs_dataframe = matchs_dataframe

    @property
    def matchs_dataframe(self):
        return self._matchs_dataframe

    @property
    def matchs_dataframes(self):
        return self._matchs_dataframes

    @matchs_dataframe.getter
    def matchs_dataframe(self):
        return self._matchs_dataframe

    @matchs_dataframes.getter
    def matchs_dataframes(self):
        return self._matchs_dataframes

    @matchs_dataframe.setter
    def matchs_dataframe(self, matchs_dataframe):
        self.__set_matchs_dataframe(matchs_dataframe)

    @matchs_dataframes.setter
    def matchs_dataframes(self, matchs_dataframes):
        self.__set__matchs_dataframes(matchs_dataframes)

    def pre_processe_matchs(self, time_limit_range=(None, None), queue_id=420,
                            selected_attributes=constants.selected_attributes):
        self.filter_matchs(time_limit_range, queue_id)
        self.feature_extraction(selected_attributes)

        return self.matchs_dataframe

    def feature_extraction(self, attributes):
        feature_extraction.set_champion_data(
            self.matchs_dataframe)

        feature_extraction.set_normalized_attributes(
            self.matchs_dataframe, attributes)

        match_count=Match_process_count(len(self.matchs_dataframes))

        self.matchs_dataframes = [feature_extraction.set_relative_attributes(
            match_dataframe, attributes, match_count) for match_dataframe in self.matchs_dataframes]

    def filter_matchs(self, time_limit_range, queue_id):
        self.matchs_dataframe = matchs_selection.filter_matchs_by_atributes(self.matchs_dataframe, time_limit_range,
                                                                            queue_id)

        self.matchs_dataframe=matchs_selection.filter_valid_matchs(self.matchs_dataframe)

    def split_matchs_by_attribute(self, attribute):
        return [dataframe for label,dataframe in self.matchs_dataframe.groupby(attribute)]

    def __set_matchs_dataframe(self, matchs_dataframe):
        self._matchs_dataframe = matchs_dataframe
        self._matchs_dataframes = [match for label, match in matchs_dataframe.groupby("gameCreation")]

    def __set__matchs_dataframes(self, matchs_dataframes):
        self._matchs_dataframes = matchs_dataframes
        self._matchs_dataframe = pd.concat(matchs_dataframes)
