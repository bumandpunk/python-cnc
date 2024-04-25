'''
Date: 2024-04-20 13:46:01
LastEditors: Zfj
LastEditTime: 2024-04-25 11:32:09
FilePath: /python-cnc/get_name2.py
Description: 
'''
import json
import base64
import requests
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
# Basic authentication with base64 encoding
def btoa(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

basic_auth = f"Basic {btoa('social:social')}"

# Fetch token for API authentication
def fetch_token(username, password):
    url = 'https://tp.cewaycloud.com/auth/oauth/token?randomStr=blockPuzzle&code=&grant_type=password'
    headers = {
        'accept': 'application/json',
        'authorization': basic_auth,
        'content-type': 'application/x-www-form-urlencoded',
        'platform-id': '1689154431733325826',
        'tenant-id': '1660451255092543490'
    }
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
    #    print('获取token成功')
       return response.json()['access_token'], response.json()['user_id']
        
    else:
        print('Error fetching token:', response.text)
        return None


# Fetch file names from the CNC table using code from shortChain data
def fetch_form_data(token, value):
            return value
 
# 轮询列表
def fetch_data(token):
    url = 'https://tp.cewaycloud.com/fd/formInstance/page'
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {token}',
        'content-type': 'application/json;charset=UTF-8',
        'platform-id': '1689154431733325826',
        'tenant-id': '1660451255092543490'
    }
    data_payload = {
        "templateId": "1781639013446074368",
        "current": 1,
        "size": 10,
        "queryFieldList":[{"fieldName":"a171384321153363681","fieldValue":"未完成","operType":"fuzzy"}],
    }
    response = requests.post(url, headers=headers, json=data_payload)
    if response.status_code == 200:
        records = response.json().get('data', {}).get('records', [])
        tuhaoList = []
        if records:
            for item in records:
                tuhaoList.append({'tuhao':item['a17138431911882915'],'id':item['id']})
            
                print('Query successful:', tuhaoList)
                return tuhaoList
        else:
            print('No records found.')
    else:
        print('Error fetching form data:', response.text)

def update_data(token,id):
    url = 'https://tp.cewaycloud.com/fd/formInstance'
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {token}',
        'content-type': 'application/json;charset=UTF-8',
        'platform-id': '1689154431733325826',
        'tenant-id': '1660451255092543490'
    }
    data_payload = {
        "id":id,
        "templateId":"1781639013446074368",
        "a171384321153363681":"已完成" 
    }
    response = requests.put(url, headers=headers, json=data_payload)
    if response.status_code == 200:
          print(id,'修改成功')
       
    else:
        print('Error fetching form data:', response.text)
def main():
    username = 'im0204'
    password = 'JFat0Zdc'
    token_data = fetch_token(username, password)
    
    if token_data:
        token, user_id = token_data
         
        # 图号列表
        result = fetch_data(token)
       
        if result :
            for item in result:
                # 更新下载状态
             print('开始更新下载状态')
             update_data(token,item['id'])
            #  fetch_form_data(token, item)
             return(fetch_form_data(token, item['tuhao']))
if __name__ == '__main__':
    main()
