import xarray as xr
import pandas as pd
import os
import numpy as np
import math
import shutil
from pandas import ExcelWriter

LAT = 31# #insert the minimum value of desire latitude
LAT_MAX = 37# #insert the maximum value of desire latitude
LONG = 245# #insert the minimum value of desire longitude
LONG_MAX = 251# #insert the maximum value of desire longitude

t1='2008-01-01' #put the starting time (yyyy-mm-dd)
t2='2016-01-31'  #put the ending time(yyyy-mm-dd)

CSR='GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409.nc'  #pathway of GRACE file of CSR
GFZ='GRCTellus.GFZ.200204_201701.LND.RL05.DSTvSCS1409.nc'  #pathway of GRACE file of GFZ
JPL='GRCTellus.JPL.200204_201701.LND.RL05_1.DSTvSCS1411.nc'  #pathway of GRACE file of JPL
SF='G:CLM4.SCALE_FACTOR.DS.G300KM.RL05.DSTvSCS1409.nc'   ##pathway of Scaling Factor

OFL='F:/arizona/oppo - Copy/'   # Output Folder location

com="Combine_GRACE"   #folder name that will give you the average value
ind="Individual_GRACE"  #folder name that will give you the individual value
##########################################################################################
###########################################################################################
def folder(folder_name):
    dir =folder_name
    if not os.path.exists(dir):
        os.makedirs(dir)
    else:
        shutil.rmtree(dir)
        os.makedirs(dir)

xc=xj=xg=x = math.floor(LAT)
pc=pj=pg=p = math.ceil(LAT_MAX)
yc=yj=yg=y = math.floor(LONG)
qc=qj=qg=q = math.ceil(LONG_MAX)

nd=OFL+'/'+ind
folder(nd)
def tws(xc,yc,pc,qc,source,CSR,SF):
    x=xc
    y=yc
    p=pc
    q=qc
    while (x<=p):
        x1=x+1
        y1=y+1
        while(y<=q):
            data = xr.open_dataset(CSR)
            vr_1 = data.sel(lat=slice(x, x1),lon=slice(y,y1),time=slice(t1,t2),bounds= slice(0,1))
            dataframe_1 = vr_1.to_dataframe()
            scaling_factor = xr.open_dataset(SF)
            vr_2 = scaling_factor.sel(Latitude=slice(x, x1),Longitude=slice(y,y1))
            dataframe_2 = vr_2.to_dataframe()
            vr_3 = dataframe_2.iat[0,0]
            k=str(x+.5)
            l=str(y+.5)
            dataframe_1.loc[:,'lwe_thickness']*=vr_3
            dataframe_4 = dataframe_1.rename(columns={'lwe_thickness':'TWS'})
            dataframe_4.to_csv(nd + '/'+source+k+'0_'+l+'0'+'.csv')
            y=y+1
            y1=y1+1
        x=x+1
        y=yc
############################################
tws(xc,yc,pc,qc,'TWS_CSR @_',CSR,SF)
tws(xc,yc,pc,qc,'TWS_GFZ @_',GFZ,SF)
tws(xc,yc,pc,qc,'TWS_JPL @_',JPL,SF)

x=xc
y=yc
p=pc
q=qc

nd1=OFL+'/'+com
folder(nd1)

x=x+0.5
y=y+0.5
FolderPath =nd+'/'
while (x<=p):
    while(y<=q):
        k=str(x)
        l=str(y)
        writer2 = ExcelWriter(FolderPath+ k+'0_'+l+'0'+'.xlsx')
        file3 = ['TWS_JPL @_','TWS_GFZ @_','TWS_CSR @_']
        for fr in file3:
            filename=  FolderPath + fr + k+'0_'+l+'0'+'.csv'
            df_csv = pd.read_csv(filename)
            (_, f_name) = os.path.split(filename)
            (f_shortname, _) = os.path.splitext(f_name)
            df_csv.to_excel(writer2, f_shortname, index=False)
        writer2.save()
        xls = pd.ExcelFile(FolderPath+ k+'0_'+l+'0'+'.xlsx')
        df1 = xls.parse(0)
        df2 = xls.parse(1)
        df3 = xls.parse(2)
        df4 = pd.DataFrame(columns=['Date','Average'])
        df4['Date']=pd.to_datetime(df2['time'],dayfirst=True).dt.date
        df4['Date']=df4['Date'].apply(lambda x:x.strftime('%m/%Y'))
        df4['Average']=(df1['TWS']+df2['TWS']+df3['TWS'])/3
        writer = ExcelWriter(nd1 + '/'+'Avergae_'+ k+'0_'+l+'0'+'.xlsx')
        df4.to_excel(writer, index=False)
        writer.save()
        y=y+1
    x=x+1
    y=math.floor(LONG)+.5
#####################