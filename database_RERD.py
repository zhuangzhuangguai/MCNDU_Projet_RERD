# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 13:07:24 2017

@author: Liu Junqing
"""

import sqlite3
#creation de la base de donnees :
'''
conn=sqlite3.connect('RERD.db')
conn.execute("create TABLE Horaire(date TEXT, time TEXT, state TEXT, num TEXT NOT NULL, mission TEXT, terminal TEXT, station TEXT NOT NULL);")
test = conn.execute("select * from Horaire limit 10;")
test.fetchall()
conn.close()
'''
def splitData(data):
    data = [i[:-1] for i in data]
    result = [i.split(',') for i in data]
    return result

def insertIntoHoraire(data):
    conn = sqlite3.connect('RERD.db')
    sql = "INSERT INTO  Horaire VALUES (?,?,?,?,?,?,?);"
    for datat in data:
        conn.execute(sql,datat)
    conn.commit()
    conn.close()
'''
file = open('C:/Users/Liu Junqing/Desktop/20171128_result_s_clean.txt','r')
data = file.readlines()
data = splitData(data)
insertIntoHoraire(data)
conn=sqlite3.connect('RERD.db')
test = conn.execute("select * from Horaire limit 10;")
test.fetchall()
conn.close()
'''    