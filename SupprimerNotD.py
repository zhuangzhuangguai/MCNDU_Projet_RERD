# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 20:43:17 2017

@author: sony
"""

import os
New_rep = "D:\\A桥路学习\\3A\\mobilité connecté\\RERD\\Result"
os.chdir(New_rep)

import codecs
import csv
with open('Listes_missions.csv', 'r', encoding = 'utf8' ) as f:
    reader = csv.reader(f)
    mission = list(reader)

del mission[0]
list_mission = []
for i in range(len(mission)):
    list_mission.append(mission[i][0][:4])


result = []
with open('20171204_result_m_clean.txt', 'r') as f:
    for line in f.readlines():
        line = line.strip('\n')
        result.append(line)

def supprimer_notD(result):
    result_clean = []
    for i in range(len(result)):
        temp = result[i][26:30]
        flag = 0
        for j in range(len(list_mission)):
            if temp == list_mission[j]:
                flag = 1
                break
        if flag == 1:
            result_clean.append(result[i])
        elif flag == 0:
            pass
    return result_clean

               
def export_data(file_name, list_name):
    f = codecs.open(file_name, 'w', 'utf-8')
    for i in list_name:
        f.write(i+"\r\n")
    f.close()
    print("Les données temps réel ont été enregistrées dans un fichier avec succès")

result_clean = supprimer_notD(result)    
export_data('20171204_result_m_traite.txt', result_clean)
