import loadjson
import pandas as pd
import numpy as np
import time
import LineNotify
from datetime import datetime

def intimecall(turnon=False):
    while True:
        df=loadjson.intimeinfo()
        a=df.loc[:,['id','value']]
        indexList=list(a.index)

        if turnon:
            for  i in indexList:
                a.xs(i)['value']=float(a['value'][i][0])
            intime=datetime.now()
            print(intime)
            intime=f'{intime}'
            intime2=(f'{intime[0:10]}-{intime[11:13]}-{intime[14:16]}')
            print(intime2)
            a.to_csv('intime.csv',index=False,sep=',')
        else:
            print(a)
            toiletList={
                'G1F_W01_Paper':'綜1F女衛生紙1',
                'G1F_W02_Paper':'綜1F女衛生紙2',
                'G1F_W03_Paper':'綜1F女衛生紙3',
                'RO1F_M01_Paper':'餐1F男衛生紙1',
                'GB1F_M01_Paper':'綜B1男衛生紙1',
                'GB1F_M02_Paper':'綜B1男衛生紙2',
                'G7F_W01_Paper':'綜7F女衛生紙1',
                'G7F_W02_Paper':'綜7F女衛生紙2',
                'G7F_W03_Paper':'綜7F女衛生紙3',
                'G7F_W04_Paper':'綜7F女衛生紙4',
                'G7F_W05_Paper':'綜7F女衛生紙5',
                'G7F_W06_Paper':'綜7F女衛生紙6',
                'G7F_W07_Paper':'綜7F女衛生紙7',
                'G7F_W08_Paper':'綜7F女衛生紙8',
                'RO1F_W01_Paper':'餐1F女衛生紙1',
                'RO1F_W02_Paper':'餐1F女衛生紙2',
                'RO1F_W03_Paper':'餐1F女衛生紙3',
                'G1F_M02_Paper':'綜1F男衛生紙2',
                'G1F_M03_Paper':'綜1F男衛生紙3',
                'G7F_M01_Paper':'綜7F男衛生紙1',
                'G7F_M02_Paper':'綜7F男衛生紙2',
                'GB1F_W01_Paper':'綜B1女衛生紙1',
                'GB1F_W02_Paper':'綜B1女衛生紙2',
                'GB1F_W03_Paper':'綜B1女衛生紙3'
            }
            for i in a['id'].values:
                a['id'][a['id']== i]=toiletList[f'{i}']

            for  i in indexList:
                a.xs(i)['value']=float(a['value'][i][0])
            shortList=a[a['value']<50.0]
            if shortList.empty:
                print('enough')
            else:
                print(shortList.values)
                LineNotify.send('gASRFTkG38DXyFWxhr7jp1lpBi9X120iZn6wA7r1IsC',f'\n  衛生紙不足:\n{shortList.values}')
                time.sleep(10)

        time.sleep(20)

if __name__=='__main__':
    intimecall(turnon=True)


