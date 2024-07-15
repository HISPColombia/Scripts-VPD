#### HISPCOLOMBIA
import requests
import json

dhis2_auth = ('user', 'passwork')###user,passwork
url = 'https://dominio_url/api/29/optionSets?fields=*&pageSize=1000'##
url2 = 'https://dominio_url/api/29/optionSets'
headers = {'Accept': 'application/json', "Content-Type": "application/json"}
response = requests.get(url, auth=dhis2_auth)
listDEupdate=[]
if response.status_code == 200:                
    data = json.loads(response.text)
    data=data['optionSets']
    for DE in data:
        unique_combinations = set()
        unique_data = []
        if len(DE['translations'])>0:
            for item in DE['translations']:
                combination = (item['locale'], item['property'])
                if combination not in unique_combinations:
                    unique_combinations.add(combination)
                    unique_data.append(item)
            if len(unique_data)<len(DE['translations']):
                DE['translations']=unique_data
                del DE['lastUpdated'], DE['href'] ,DE['created']
                print(DE)
                responseUpdate = requests.put(url2+'/'+DE['id'], data=json.dumps(DE), auth=dhis2_auth, headers=headers)
                print(url2+'/'+DE['id'])
                if responseUpdate.status_code == 200:
                    print ("Entity correctly updated :" + responseUpdate.text)
                    listDEupdate.append(DE['id'])
                else:
                    print("Error: Unable to update PUT record : ====================== \n" + responseUpdate.text)
                    print(responseUpdate.json)
                    print(responseUpdate.status_code)
print(listDEupdate)
