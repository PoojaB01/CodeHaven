from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import requests
import json
import csv
import sys
import os

sys.path.append(r'.')
# with open('Ladder4.csv', 'r') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         # print(row)

def get_ladder(user, number):
    handle = user 
    link = "https://codeforces.com/api/user.status?handle="+handle
    # print(link)
    cf_api = requests.get(link)

    Ques = cf_api.json()['result']

    UserQ = set()

    for data in Ques:   
        if data["verdict"]=='OK':
            UserQ.add(" "+str(data["problem"]["contestId"])+"/ "+data["problem"]["index"])
        
            #print(str(data["problem"]["contestId"])+'/'+data["problem"]["index"])
    cnt = 0
    LadQ = []
    with open('crawler//Data//Ladder' + str(number) + ".csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            ques = {}
            ques['SNo'] = row[0]
            ques['name'] = row[1]
            ques['link'] = row[2]
            cnt = cnt + 1
            if cnt == 1 or str(str(row[3])+'/'+row[4]) in UserQ:
                if cnt>1:
                    LadQ.append(ques)
                    #print(str(row[3])+'/'+row[4])
            else :
                LadQ.append(ques)
                #print(str(str(row[3])+'/'+row[4]))
                break


    #result = UserQ.intersection(LadQ)
    # print(result)
    # print(UserQ)
    # print(LadQ)
    return LadQ
