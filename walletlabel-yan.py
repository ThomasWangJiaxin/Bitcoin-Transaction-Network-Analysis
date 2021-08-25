# coding=utf8
from bs4 import BeautifulSoup
import requests
import csv
import time
import random
import datetime
import pandas as pd
import numpy as np
from requests.adapters import HTTPAdapter
user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15"
    ]

#输入要爬的地址addlist
#inputs=pd.read_csv('aqb_tx_in_out_add.csv')
#outputs=pd.read_csv('aqb_tx_out_out_add.csv')
# addlist_terror=list(set(inputs['input_address'].tolist()+outputs['output_address'].tolist()))
aq = pd.read_csv('alladdonelevel.csv')
do_adds = aq['address'].tolist()
#do_input = inputs[inputs['txid'].isin(outputs[outputs['output_address'].isin(do_adds)]['txid'].tolist())]['input_address'].unique().tolist()
#edge_new_df_trace=pd.read_csv('aqb_3_alladd/aqb_tracefrom3.csv')
#edge_new_df=pd.read_csv('aqb_3_alladd/aqb_traceto3.csv')
#addlist_trace=list(set(edge_new_df['source'].tolist()+edge_new_df['target'].tolist()))
#addlist_tracefrom=list(set(edge_new_df_trace['source'].tolist()+edge_new_df_trace['target'].tolist()))
#addlist = list(set(do_input + addlist_trace + addlist_tracefrom))
addlist = list(set(do_adds))


while np.nan in addlist:
    addlist.remove(np.nan)
print('地址数：',len(addlist))
#print(wallet_style)
#print(len(wallet_style))
success_list = []
wallet_list=[]
last_request = ''
requests.DEFAULT_RETRIES = 5  # 增加重连次数
s = requests.session()
s.mount('http://', HTTPAdapter(max_retries=9))
s.mount('https://', HTTPAdapter(max_retries=9))
# s.keep_alive = False
index = 0
while index < len(addlist):
    if addlist[index] in success_list:
        index = index + 1
        continue
    else:
        try:
            print(addlist[index])
            start_time = datetime.datetime.now()
            api_index = 'http://www.walletexplorer.com/api/1/address-lookup?address=' + addlist[index] + '&caller=mf1914072@smail.nju.edu.cn'
            wa_content = s.get(api_index, headers={'User-Agent': random.choice(user_agent_list)}, timeout=(50,160)).json()
            time.sleep(2)
            print("标签获取完毕",addlist[index],wa_content['wallet_id'])
            success_list.append(addlist[index] )
            print("已完成：" ,len(success_list))
            if wa_content:
                if 'label' in wa_content.keys():
                    wallet_list.append([addlist[index], wa_content['wallet_id'], wa_content['label']])
                else:
                    wallet_list.append([addlist[index], wa_content['wallet_id'], ''])
                with open('wa5/' + addlist[index] + '.csv', 'w', newline='')as f:
                #with open('wa5/addlist.csv', 'w', newline='')as f:
                    writer = csv.writer(f)
                    writer.writerow(["address", "wallet_id", "label"])
                    if 'label' in wa_content.keys():
                        writer.writerow([addlist[index], wa_content['wallet_id'], wa_content['label']])
                    else:
                        writer.writerow([addlist[index], wa_content['wallet_id'], ''])
            end_time = datetime.datetime.now()
            seconds = (end_time - start_time).seconds
            start = start_time.strftime('%Y-%m-%d %H:%M')
            # 100 秒
            # 分钟
            minutes = seconds // 60
            second = seconds % 60
            print((end_time - start_time))
            timeStr = str(minutes) + '分钟' + str(second) + "秒"
            print('运行时间为：' + timeStr)
        except Exception as e:
            print(addlist[index])
            print("获取首条记录出现异常:" + str(e) + "那就休息1秒")
            time.sleep(1)
wallet_id_df=pd.DataFrame(wallet_list,columns=['address','wallet_id','label'])
wallet_id_df.to_csv('wa5/wallet_id_df2.csv',index=False,header=True)
print("全部结束！")

