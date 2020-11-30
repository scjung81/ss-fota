#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib as mpl
import matplotlib.pylab as plt
# import seaborn as sns  ## matplotlib 쓰기 어려우므로 간결한 사용가능함.
import numpy as np
import os

import re


# In[2]:


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# In[3]:

def StartMakeDb_current():
    #마지막 폴더 찾기
    filepath = "data"
    # lastdate = max([filepath +"/"+ f for f in os.listdir(filepath)], key=os.path.getctime)
    lastdate = max([filepath +"/"+ f for f in os.listdir(filepath) if re.match(r'[^.]+', f)], key=os.path.getctime)
    dt = lastdate.split("/")[1].split("_")[0]
    time = lastdate.split("_")[1]

    print(lastdate, dt,time)


    # In[20]:


    ss_fota = pd.read_excel(os.path.join(os.getcwd(),lastdate,f"ss_fota_real_time_{dt}_{time}.xlsx"),header = 3, na_values = 'NaN')
    ss_fota['sync_dt'] = dt
    ss_fota['sync_time'] = time

    ss_fota


    # In[21]:
    #S20+ BTS edition 예외처리, Model명 변경
    sw_ver = ss_fota['Current Version'].str.contains('/', regex=False, na=False)
    s20_bts = (ss_fota['Model'] == 'SM-G986N') & (ss_fota.loc[sw_ver, 'Current Version'].str.split("/").str[1].str[-8:-5] == 'OKT')
    ss_fota.loc[(sw_ver & s20_bts), 'Model'] = 'SM-G986N-BTS'



    #모델별 Total count 추가
    tot_device_count = ss_fota["Total Count"].groupby([ss_fota["Model"]]).sum().reset_index()
    tot_device_count.rename(columns = {'Total Count' : "Total Device Count_with_OTHERS"}, inplace = True)

    tot_device_count
    merged = pd.merge(ss_fota, tot_device_count)
    merged["MS_with_OTHERS"] = merged["Total Count"]/merged["Total Device Count_with_OTHERS"]*100
    ss_fota = merged


    # In[22]:


    ss_fota.dtypes


    # In[23]:


    sw_ver = ss_fota['Current Version'].str.contains('/', regex=False, na=False)
    ss_fota['ap'] = ss_fota['Current Version']
    ss_fota.loc[sw_ver, 'ap'] = ss_fota.loc[sw_ver,'Current Version'].str.split("/").str[0].str[-3:]
    ss_fota.loc[sw_ver, 'cp'] = ss_fota.loc[sw_ver,'Current Version'].str.split("/").str[2].str[-3:]
    ss_fota['ap_cp'] = ss_fota['ap'] + "_" + ss_fota['cp']
    ss_fota.loc[ss_fota['cp'].isnull(), 'ap_cp'] =  ss_fota.loc[ss_fota['cp'].isnull(), 'ap']

    ss_fota.head()


    # In[24]:


    pivot = pd.pivot_table(ss_fota, index=['Model','ap','cp','ap_cp'])
    df = pivot.reset_index()
    df


    # In[25]:


    # model_list = ["SM-G977N", "SM-N976N"]
    # ss_fota_data = ss_fota.loc[ss_fota["Model"].isin(model_list)]
    ss_fota_data = ss_fota
    ss_fota_data = ss_fota_data.sort_values(by=["Model", "ap_cp"])


    # In[26]:


    def getNew_plm_sw():
        #마지막 폴더 찾기
        filepath = f"{os.path.abspath('..')}\\plm_selenium\\crawling\\data"
        lastdate = max([filepath +"/"+ f for f in os.listdir(filepath)], key=os.path.getctime)
        print(lastdate)

        path = os.path.join(os.getcwd(), lastdate, "plm_swver_DataWarehouse.xls")
        print(path)
        df = pd.read_excel(path)
        print(df.shape)
        return df


    # In[27]:


    ss_fota_data.loc[ss_fota_data["Model"] == 'SM-G977N']


    # # PLM 정보 통합

    # In[28]:


    plm_sw = getNew_plm_sw()
    plm_sw.head()


    # In[29]:


    col = ['manufacturer', 'pet_name', 'model', 'ua_model', 'ua_ver', 'ue_type', 'acceptance_date', 'release_sw', 'ongoing', 'release_type', 'os_type', 'os_ver', 'codeName']
    plm_sw= plm_sw.loc[plm_sw['manufacturer']=='삼성전자', col]
    plm_sw.head()


    # In[30]:


    a1 = pd.merge(ss_fota_data, plm_sw, left_on=['Model', 'ap_cp'], right_on=['model', 'ua_ver'], how='inner' )
    a2 = pd.merge(ss_fota_data, plm_sw, left_on=['Model', 'ap'], right_on=['model', 'ua_ver'], how='inner' )


    # In[31]:


    ss_fota_final = pd.concat([ss_fota_data, a1, a2], sort=False)
    ss_fota_final = ss_fota_final.drop_duplicates(["Model", "ap_cp"], keep='last').sort_values(by=["Model", "ap_cp"])
    ss_fota_final.head()

    # 외부팀 비공개 버전 예외 처리
    except_sw = list()
    except_sw.append({'model': "SM-G977N", "ap_cp": ["SD1_SD1", "SD1_SD4"]})
    print(except_sw)

    for excetp in except_sw:
        ss_fota_final.loc[
            (ss_fota_final["model"] == excetp['model']) & (ss_fota_final["ap_cp"].isin(excetp['ap_cp'])), [
                "release_sw"]] = np.nan


    # In[32]:


    ss_fota=ss_fota_final.loc[ss_fota_final["release_sw"].notnull()]

    #모델별 Total count 추가
    tot_device_count = ss_fota["Total Count"].groupby([ss_fota["Model"]]).sum().reset_index()
    tot_device_count.rename(columns = {'Total Count' : "Total Device Count"}, inplace = True)

    tot_device_count
    merged = pd.merge(ss_fota_final, tot_device_count)
    merged["MS"] = merged["Total Count"]/merged["Total Device Count"]*100
    ss_fota_final = merged
    ss_fota_final


    # In[33]:


    lstday = lastdate.split("/")[1]
    fname  = lastdate+"/ss_fota_current_" + lstday + ".csv"
    fname2  = lastdate+"/ss_fota_current.csv"
    print(fname, fname2)

    ss_fota_final.to_csv(fname, encoding='euc-kr', index=False)
    ss_fota_final.to_csv(fname2, encoding='euc-kr', index=False)


## Start
if __name__ == "__main__":
    StartMakeDb_current()




