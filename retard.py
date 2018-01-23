# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
data = pd.read_csv('C:/Users/Liu Junqing/Desktop/semaine1.txt',sep=',',encoding='cp1252',header=None)
data.columns=('t_date','t_time_theorique','type_horaire','num_train','mission','terminus','gare','etat_theorique','t_extraction_theorique','t_time_reel','etat_reel','t_extraction_reel','retard')
data = data.drop_duplicates()
data['retard']=data['retard'].apply(pd.to_numeric)

data['t_date']=pd.to_datetime(data['t_date'],format="%d/%m/%Y").dt.date
data['t_time_theorique']=pd.to_datetime(data['t_time_theorique'],format="%H:%M").dt.time

gares = pd.read_csv('C:/Users/Liu Junqing/Desktop/gares.csv',sep=';',header=None)
gares.columns=('name','gare')

data = pd.merge(data,gares,on='gare')
data.rename(columns={'name': 'gare_name'}, inplace=True)
#gares.columns=('name','terminus')
#data = pd.merge(data,gares,on='terminus',how='left')
#data.rename(columns={'name': 'terminus_name'}, inplace=True)

data['gare']=data['gare'].astype('category')
data['terminus']=data['terminus'].astype('category')
data['gare_name']=data['gare_name'].astype('category')
#data['terminus_name']=data['terminus_name'].astype('category')
data = data.sort_values(['t_time_theorique'],ascending=True)
df=data[['num_train','mission','terminus','t_date','t_time_theorique','gare','retard','gare_name']]
#---------------------------------------------------------------
#images
#---------------------------------------------------------------
#tous les retards pendant la semiane
ls = list(df.groupby(['num_train','mission','terminus']))
for lls in ls:
    if lls[1]['retard'].sum()!=0.0:
        #lls=ls[99]
        tl = "{},{},{}".format(lls[0][0],lls[0][1],lls[0][2])
        rett= lls[1][['gare_name','t_date','retard']]
        #rett = rett.set_index('gare_name')
        #rett = rett.reset_index(drop=True)
        rett = rett.pivot(index='gare_name',columns='t_date')['retard']
        pic = rett.plot(subplots=True,sharex=True,legend=True,use_index=True,title=tl,marker='.',markersize=15)
        pic[0].set_xticks(np.arange(len(rett)))
        pic[0].set_xticklabels(rett.index,rotation=90)
        fig = pic[0].get_figure()
        fig.set_size_inches(30, 25)
        name = "{}_{}_{}".format(lls[0][0],lls[0][1],lls[0][2])
        fig.savefig(fname='pct/'+name+'.png',dpi=100)
-------------------------------------------------------------------
#la moyenne de retard pendant la semaine
ls = list(df.groupby(['num_train','mission','terminus','gare_name']))
re =list()
for lss in ls:
    #lss = ls[1]
    re.append((lss[0][0],lss[0][1],lss[0][2],lss[0][3],lss[1]['retard'].mean()))
redf = pd.DataFrame(re)
redf.columns=('num_train','mission','terminus','gare_name','retard_moyen')
ls = list(redf.groupby(['num_train','mission','terminus'])) 
plt.close("all")
for lss in ls:
    if lss[1]['retard_moyen'].sum()!=0:
        tl = "{},{},{}".format(lss[0][0],lss[0][1],lss[0][2])
        rett= lss[1][['gare_name','retard_moyen']]
        rett = rett.set_index('gare_name')
        pic = rett.plot(subplots=False,legend=True,use_index=True,title=tl,marker='.',markersize=15)
        pic.set_xticks(np.arange(len(rett)))
        pic.set_xticklabels(rett.index,rotation=90)
        fig = pic.get_figure()
        fig.set_size_inches(30, 25)
        name = "{}_{}_{}".format(lss[0][0],lss[0][1],lss[0][2])
        fig.savefig(fname='pct/'+name+'.png',dpi=100)
#-------------------------------------------------------------------
#mas de retard pendant la semaine
ls = list(df.groupby(['num_train','mission','terminus','gare_name']))
re =list()
for lss in ls:
    #lss = ls[1]
    re.append((lss[0][0],lss[0][1],lss[0][2],lss[0][3],lss[1]['retard'].max()))
redf = pd.DataFrame(re)
redf.columns=('num_train','mission','terminus','gare_name','retard_max')
ls = list(redf.groupby(['num_train','mission','terminus'])) 
plt.close("all")
for lss in ls:
    if lss[1]['retard_max'].sum()!=0:
        tl = "{},{},{}".format(lss[0][0],lss[0][1],lss[0][2])
        rett= lss[1][['gare_name','retard_max']]
        rett = rett.set_index('gare_name')
        pic = rett.plot(subplots=False,legend=True,use_index=True,title=tl,marker='.',markersize=15)
        pic.set_xticks(np.arange(len(rett)))
        pic.set_xticklabels(rett.index,rotation=90)
        fig = pic.get_figure()
        fig.set_size_inches(30, 25)
        name = "{}_{}_{}".format(lss[0][0],lss[0][1],lss[0][2])
        fig.savefig(fname='pct/'+name+'.png',dpi=100)