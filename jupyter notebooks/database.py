import pandas as pd
import numpy as np
import requests

database_path="../../datasets/ranked_dataset.csv"

def set_champions_data():
    database=pd.read_csv(database_path)
    champions_json=requests.get(b'http://ddragon.leagueoflegends.com/cdn/8.13.1/data/en_US/champion.json').json()
    champions_data=champions_json["data"].values()
    champions_dict={
        "champion_name":[],"champion_attack":[],"champion_defense":[],
        "champion_magic":[],"champion_difficulty":[],"champion_class":[],
        "champion_subclass":[]
    }
    champions_data_keys=["champion_name","champion_attack","champion_defense","champion_magic","champion_difficulty"
                         ,"champion_class","champion_subclass"]

    for key_champion in database["champion"]:
        for champion in champions_data:
            if(key_champion==int(champion["key"])):
                array_data=[champion["id"]]
                [array_data.append(value) for value in champion["info"].values()]
                if(len(champion["tags"])==2):
                    array_data.append(champion["tags"][0])
                    array_data.append(champion["tags"][1])
                else:
                    array_data.append(champion["tags"][0])
                    array_data.append(champion["tags"][0])
                for key,value in zip(champions_data_keys,array_data):
                    champions_dict[key].append(value)
                print(array_data)
    for key in champions_data_keys:
        database[key]=champions_dict[key]

    database.to_csv(database_path,index=False,index_label=False)



set_champions_data()
