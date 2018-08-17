import os

selected_attributes = ["assists", "deaths", "goldEarned", "kills", "longestTimeSpentLiving", "magicDamageDealt",
                      "magicalDamageTaken", "neutralMinionsKilled", "physicalDamageDealt", "physicalDamageDealtToChampions",
                      "physicalDamageTaken", "timeCCingOthers", "totalDamageDealt", "totalDamageDealtToChampions",
                      "totalDamageTaken", "totalHeal", "totalMinionsKilled", "totalTimeCrowdControlDealt", "trueDamageDealt",
                      "trueDamageDealtToChampions", "trueDamageTaken", "visionScore", "visionWardsBoughtInGame", "wardsPlaced"]

rel_selected_attributes=["rel_"+attribute for attribute in selected_attributes]
norm_selected_attributes=["norm_"+attribute for attribute in selected_attributes]

champion_info = ["champion_name", "champion_difficulty", "champion_defense", "champion_attack",
                 "champion_magic", "champion_class", "champion_subclass"]

lanes_positions=["adc", "jg", "mid", "sup", "top"]

ROOT_URL = os.path.abspath(__file__)
champions_json_path = os.path.join(os.path.dirname(ROOT_URL), "static/champion.json")