#table paths
path_dataset="../datasets/ranked_dataset.csv"
path_treated_dataset="../datasets/treated_dataset.csv"
path_routes_datasets="../datasets/routes/"
path_table_files="tabelas/"
path_info_routes="tabelas/informações dos dados das rota.csv"
path_routes_importance="tabelas/importancia das rotas.csv"
path_models_crossvalidation_score="tabelas/cross validation score.csv"
path_estatisticas_atributos="tabelas/estatisticas atributos.csv"
path_correlacoes_atributos="tabelas/correlacões atributos.csv"
path_tabelas_rotas="tabelas/rotas/"

#images paths
image_root_path="images/"
file_statistics="images/estatisticas/"
file_correlation="images/correlacao/"
file_histograms="images/histogramas/"
file_distribuition="images/distribuicao/"
file_selected_features="images/selected_features/"
file_heatmap="images/mapa de calor das correlações.png"
file_cross_validation_acuracy="images/cross validation score.png"
file_cross_validation_std="images/cross validation std.png"
file_routes_importance="images/router importance.png"


#atributes variables
atributos_numericos=["assists","deaths","goldEarned","kills","longestTimeSpentLiving","magicDamageDealt",
                     "magicalDamageTaken","neutralMinionsKilled","physicalDamageDealt","physicalDamageDealtToChampions",
                     "physicalDamageTaken","timeCCingOthers","totalDamageDealt","totalDamageDealtToChampions",
                     "totalDamageTaken","totalHeal","totalMinionsKilled","totalTimeCrowdControlDealt","trueDamageDealt",
                     "trueDamageDealtToChampions","trueDamageTaken","visionScore","visionWardsBoughtInGame","wardsPlaced"]

atributos_numericos_relativos=["rel_"+atribute for atribute in atributos_numericos]

atritubos_numericos_normalizados=["norm_"+atribute for atribute in atributos_numericos]

atributos_pesos=[1,-1,1,1,1,1,-1,1,1,1,-1,1,1,1,1,1,1,1,1,1,1,1,1,1]

atributos_pesos_dict={atributo:peso for atributo,peso in zip(atributos_numericos,atributos_pesos)}

#normal variables
rotas_labels=["DUO_CARRY","DUO_SUPPORT","MIDDLE","JUNGLE","TOP"]
rotas_names=["adc","sup","mid","jg","top"]
rotas_cmaps=["Reds","Blues","Greens","Oranges","Purples"]
