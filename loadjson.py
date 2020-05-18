import requests
import json
import pandas as pd

def loaddeviceinfo():
    response=requests.get('https://iot.cht.com.tw/iot/v1/metadata',
        headers={
            'CK':'PKRXHT12BS0C0G2TCZ',
        }
    )

    if response.status_code !=200:
        print(f'download Json list failed {response.status_code}')
    
    else:
        info=json.loads(response.text)
    
    return info

def getdeviceID():
    info=loaddeviceinfo()
    dataframeinfo=pd.json_normalize(info)
    idselect=dataframeinfo.loc[:,"id"]
    deviceID=idselect.values
    return deviceID

def intimeinfo():
    deviceID=getdeviceID()
    intimevalue=pd.DataFrame(columns=['id','deviceId','time','value'])
    for ID in deviceID:
        response=requests.get(f'https://iot.cht.com.tw/iot/v1/device/{ID}/rawdata',
            headers={
                'CK': 'PKRXHT12BS0C0G2TCZ',
            }
        )
        if response.status_code !=200:
            print(f'download Json list failed {response.status_code}')
    
        else:
            info=json.loads(response.text)
            dataframeinfo=pd.json_normalize(info)
            intimevalue=pd.concat([intimevalue,dataframeinfo],ignore_index=True)
    return intimevalue




if __name__ == '__main__':
    intimeinfo()