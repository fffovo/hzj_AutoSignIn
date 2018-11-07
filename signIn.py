# Created at 2018.11.07 by Ultraxia

import requests
import pymysql
import json
import time

header = {'User-Agent': 'Mozilla/5.0 (Linux; Android 9.0; MI 8 Build/PKQ1.180729.001; wv) \
                    AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044306 Mobile Safari/537.36'}


def getSchoolid():
    url = 'http://gzdk.gzisp.net/api/getSchoolListWeb?authorization='
    response = requests.post(url).json()
    if response['res'] == 'success':
        schoolData = response['data']
        for values in schoolData.values():
            for school in values:
                if school['schoolName'] == schoolName:
                    schoolId = school['schoolId']
                    return schoolId


def login():
    url = 'http://gzdk.gzisp.net/api/authenticateNew'
    form = {'username': username,
            'password': password,
            'schoolId': schoolId}
    response = requests.post(url, form, headers=header).json()
    if response['res'] == 'succ':
        userName = response['data']['userName']
        token = list(set({response['data']['id_token']}))[0]
        token = {'userName': userName, 'token': token}
        return token
    else:
        print('登陆失败！请检查账号密码是否正确')


def checkSign():
    tokenData = login()
    token = tokenData['token']
    url = 'http://gzdk.gzisp.net/sign/getMyCheckinSubList?authorization={}'
    url = url.format(token)
    response = requests.get(url, headers=header).json()
    if response['res'] == 'success':
        data = response['data'][1][0]
        address = data['label']
        locationX = data['locationX']
        locationY = data['locationY']
        signData = {'address': address, 'token': token, 'locationX': locationX, 'locationY': locationY}
        return signData
    else:
        print(response['desc'])


def signAction():
    signData = checkSign()
    token = signData['token']
    address = signData['address']
    locationX = signData['locationX']
    locationY = signData['locationY']
    url = 'http://gzdk.gzisp.net/sign/addSignIn?ADDR={}&AXIS={}-{}&CONTENT=&IDS=&ISEVECTION=0&SCALE=18&authorization={}'
    url = url.format(address, locationY, locationX, token)
    response = requests.get(url, headers=header).json()
    if response['res'] == 'success':
        print('签到成功！')


if __name__ == '__main__':
    username = ''
    password = ''
    schoolName = ''
    schoolId = getSchoolid()
    signAction()

