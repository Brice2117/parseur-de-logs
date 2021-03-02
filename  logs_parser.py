#!/usr/bin/env python
# coding: utf-8

import re # utiliser pour la definition des patterns
import sys
import pandas as pd # Librairie de manipulation de données


# In[138]:


try:
    import pandas
except ImportError:
        input("Cannot load module pandas. Press enter to install the package pandas or Ctrl+c to quit the program")
        os.system("pip3 install --user pandas")
        import pandas as pd # Librairie de manipulation de données



def get_and_preprocess_data(fileName):
    # On charge les données du fichier dans un data frame en prenant le soin de mettre le paramettre 'header' à None
    # header=None nous permet d'évité que la première ligne soit considérer comme les noms de colonnes
    df = pd.read_csv(fileName, delimiter="\t", header=None)
    
    print("============ Nombre de lignes avant suppression des url non tuile ====== ----> ", str(len(df)))
    
    # on affecte un nom à chacune de nos colonnes
    columnsName = ['datetime', 'viewmode']
    df.columns = columnsName
    
    # On ne retient que les données avec dea urls correspondent  à une tuile
    df = df[df['viewmode'].str.contains("/map/1.0/slab/", na=False)].reset_index(drop=True)
    
    print("============ Nombre de lignes après suppression des url non tuile ====== ----> ", str(len(df)))
    
    return df


# In[136]:


def get_list_of_unique_viewmode(dataFrame):
    
    # On crée un pattern qui nous va nous permttre d'aller recupérer les viewmode
    pattern = "slab/(.*?)/"
    # On crée un set pour y stocker les viewmode de façon unique
    list_viewmode = set()
    
    for index in range(len(dataFrame)):
        list_viewmode.add(re.search(pattern, dataFrame['viewmode'][index]).group(1))
    
    list_viewmode = list(list_viewmode)
    print('======= Liste des viewmode =========')
    print(list_viewmode)
    
    return list_viewmode


# In[134]:


def zoom_level_of_each_viewmode(dataFrame, list_viewmode):
    # On crée un pattern qui nous va nous permttre d'aller les viewmode
    pattern = "/256/(.*?)/"
    list_zoom_level = list()
    temp_dct = {"viewmode":[],"occurence":[], 'Niveau de zoom':[]}
    
    for view_m in list_viewmode:
        temp_dataFrame = dataFrame[dataFrame['viewmode'].str.contains(str(view_m), na=False)
                                  ].reset_index(drop=True)
        occur = len(temp_dataFrame)
        for index in range(len(temp_dataFrame)):
            list_zoom_level.append(re.search(pattern, temp_dataFrame['viewmode'][index]).group(1))
        temp_dct['viewmode'].append(view_m)
        temp_dct['occurence'].append(occur)
        temp_dct['Niveau de zoom'].append(','.join(map(str, set(list_zoom_level))))
        
        # On renitialise la liste à chaque boucle
        list_zoom_level = []
    df_viewmode_occu = pd.DataFrame.from_dict(temp_dct)

    return df_viewmode_occu


if __name__ == "__main__":
    # chargemnt du fichier de données
    print('\n')
    data = get_and_preprocess_data("tornik-map-20171006.10000.tsv")

    # Récupération de la liste des viewmode
    print('\n')
    list_viewmode = get_list_of_unique_viewmode(data)

    # Raffinage des logs
    df_viewmode_occu = zoom_level_of_each_viewmode(data, list_viewmode)

    # Affichage du jeux de de données(résultats)
    print('\n')
    print(df_viewmode_occu.to_string(index=False))





