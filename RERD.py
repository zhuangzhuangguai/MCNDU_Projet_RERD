# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 19:53:19 2017

@author: sony
"""

import requests
import pandas as pd
import xml.etree.ElementTree as ET
import time
from time import sleep
from datetime import datetime

import os
New_rep = "C:/Users/sony/Desktop/RERD"
os.chdir(New_rep)


Nb_boucles = 3
Sleep_time = 60
#Le temps de point au matin : 5h55 - 10h05, 4h10min au total, 250min, donc 250 boucles avec 60s de pause entre chaque deux requetes.
#Le temps de point au soir : 15h55 - 20h05, 4h10min au total, 250min, donc 250 boucles avec 60s de pause entre chaque deux requetes.

login_id = ["tnhtn730", "tnhtn703", "tnhtn729"]
login_mdp = ["kM2q8Xa2", "4g6qVRy3", "iP3Yu2x7"]



import csv
with open('Gares.csv', 'r') as f:
    reader = csv.reader(f)
    Gares = list(reader)
f.close()

del Gares[0]
list_gares_id = []
for i in range(len(Gares)):
    list_gares_id.append(Gares[i][0][:8])
#Il y a 60 gares au total.    

 
##with open('Missions_descriptions.csv','r') as fichier:
##    reader = csv.reader(fichier)    
##    Missions=list(reader)
##fichier.close()


def requete(list_gare_id, login, mdp):
    list_train = list()
    for gare_id in list_gare_id:
        adresse_api="http://api.transilien.com/gare/"+gare_id+"/depart/"
        r = requests.get(adresse_api, auth=(login, mdp))
        root = ET.fromstring(r.text)
        for train in root:
            stl = '{},{},{},{},{},{},{}'.format(train[0].text[:10],train[0].text[11:],train[0].attrib['mode'],train[1].text,train[2].text,train[3].text,gare_id)
            list_train.append(stl)
    return list_train

##test = requete(gares[0:19], "tnhtn703", "4g6qVRy3")
##len(test)
    

def Secondes(temps_str):
    return int(temps_str[0:2])*3600+int(temps_str[3:5])*60+int(temps_str[6:8])



def extract_horaires_api(delta, list_gares_id, login_id, login_mdp):
    time.sleep(delta)
    result = []
    print("Début à " + str(datetime.now())[11:19])
    for i in range(0,Nb_boucles):
        print("Début requête à " + str(datetime.now())[11:19])
        t_start=str(datetime.now())[11:19]
        temp1 = requete(list_gares_id[:20], login_id[0], login_mdp[0])
        temp2 = requete(list_gares_id[21:40], login_id[1], login_mdp[1])
        temp3 = requete(list_gares_id[41:60], login_id[2], login_mdp[2])
        result.extend(temp1)
        result.extend(temp2)
        result.extend(temp3)
        t_end=str(datetime.now())[11:19]
        print("Fin enregistrement requête dans la liste à " + str(datetime.now())[11:19])
        if Sleep_time>(Secondes(t_end)-Secondes(t_start)):
            time.sleep(Sleep_time-(Secondes(t_end)-Secondes(t_start)))
    print("Fin à " + str(datetime.now())[11:19])
    print ("Les données temps réel ont été enregistrées dans la liste avec succès")
    return result

def supprimer_doublon(result_brut):
    result_clean = []
    result_clean.append(result_brut[0])
    for i in range(1,len(result_brut)):
        num = result_brut[i][19:25]
        gare = result_brut[i][40:48]
        flag = 0
        for j in range(len(result_clean)):
            num_c = result_clean[j][19:25]
            gare_c = result_clean[j][40:48]
            if num == num_c and gare == gare_c:
                result_clean[j] = result_brut[i]
                flag = 1
                break
        if flag == 0:
            result_clean.append(result_brut[i])
        elif flag ==1:
            pass
    return result_clean

#Je vous conseille d'écrire cette fonction comme ci-dessous, il marche plus vite
#juste quelques secondes pour les données brutes du matin
'''           
def supprimer_doublon(result_list):
    result = result_list
    for i in range(1,len(result)):
        for re in result[0:-i]:
            if re[19:25] == result[-i][19:25] and re[40:48] == result[-i][40:48]:            
                result.remove(re)
    return result
'''
        
        
delta_HPM = Secondes("05:55:00")-Secondes(str(datetime.now())[11:19])+Secondes("24:00:00")
delta_HPS = Secondes("15:55:00")-Secondes(str(datetime.now())[11:19])+Secondes("24:00:00")
    

result_m = extract_horaires_api(delta_HPM, list_gares_id, login_id, login_mdp)

result_s = extract_horaires_api(delta_HPS, list_gares_id, login_id, login_mdp)

result_m_clean = supprimer_doublon(result_m)

result_s_clean = supprimer_doublon(result_s)


f=open('20171126_result_m.txt','w')
for i in result_m:
    f.write(i+"\n")
f.close()


f=open('20171126_result_s.txt','w')
for i in result_s:
    f.write(i+"\n")
f.close()

f=open('20171126_result_m_clean.txt','w')
for i in result_m_clean:
    f.write(i+"\n")
f.close()

f=open('20171126_result_s_clean.txt','w')
for i in result_s_clean:
    f.write(i+"\n")
f.close()




'''test = extract_horaires_api(60, list_gares_id, login_id, login_mdp)
test_clean = supprimer_doublon(test)
f=open('result_test.txt','w')
for i in test:
    f.write(i+"\n")
f.close()

f=open('result_test_clean.txt','w')
for i in test_clean:
    f.write(i+"\n")
f.close()'''



#root[0][0].text
#root[1][0].text
#root[29][0].text
