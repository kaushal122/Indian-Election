import pandas as pd
from bs4 import BeautifulSoup
import requests
import streamlit as st
# This fucntion returns pandas dataframe of seats party wise
def state_result(state,url):
    dict = {"Andhra Pradesh": "S01", "Assam": "S03", "Bihar": "S04", "Goa": "S05", "Haryana": "S07",
            "Himachal Pradesh": "S08", "Karnataka": "S10", "Madhya Pradesh": "S12", "Maharashtra": "S13",
            "Manipur": "S14", "Meghalaya": "S15", "Mizoram": "S16", "Nagaland": "S17", "Punjab": "S19",
            "Rajasthan": "S20", "Uttar Pradesh": "S24", "Uttarakhand": "S28", "Telangana": "S29", "West Bengal": "S25",
            "Dadra & Nagar Haveli And Daman & Diu": "U04"}

    base_url = "https://results.eci.gov.in/"+url+dict[state]+".htm?st="+dict[state]

    response  = requests.get(base_url)

    html = response.content

    soup = BeautifulSoup(html,'lxml')


    r = soup.find_all('table',)


    useful = r[8]


    text = useful.text

    n = r[8].find_all('th')



    columns=[]
    for i in range(0,len(n)):
        columns.append(n[i].string)

    href = ['ResultAcByeNov2021/partywiseresult-S01.htm', 'ResultPcByeNov2021/partywiseresult-U04.htm','ResultAcGenMar2022/partywiseresult-S05.htm', 'ResultAcByeMar2022/partywiseresult-S03.htm']
    text = ['Bye Elections to Assembly Constituency November-2021 ',
                'Bye Elections to Parliament Constituency November-2021 ']



    m = r[8].find_all('td')
    lst = []
    for i in m:
        lst.append(i.text.strip())
    if url==href[1][0:href[1].index("-")+1]:
        columns = columns[2:]

        # if url!=href[1][0:href[1].index("-")+1]:
        #     l = lst[0].index("\n")



    list =[]
    if url!=href[1][0:href[1].index("-")+1]:
        n = (int)((len(lst)-2)/4)
        for i in range(0,n):
            row=lst[2+4*i:2+4*i+4]
            list.append(row)
        data = pd.DataFrame(list,columns = columns)
        data.index+=1
    else:
        n = (int)((len(lst))/4)
        for i in range(0,n):
            row=lst[4*i:4*i+4]
            list.append(row)
        data = pd.DataFrame(list,columns = columns)
        data[['Won', 'Leading', 'Total']] = data[['Won', 'Leading', 'Total']].apply(pd.to_numeric)
        data.index+=1
    return (data)



#this functions returns party wise vote share
def votes(state, url):
    dict = {"Andhra Pradesh": "S01", "Assam": "S03", "Bihar": "S04", "Goa": "S05", "Haryana": "S07",
            "Himachal Pradesh": "S08", "Karnataka": "S10", "Madhya Pradesh": "S12", "Maharashtra": "S13",
            "Manipur": "S14", "Meghalaya": "S15", "Mizoram": "S16", "Nagaland": "S17", "Punjab": "S19",
            "Rajasthan": "S20", "Uttar Pradesh": "S24", "Uttarakhand": "S28", "Telangana": "S29", "West Bengal": "S25",
            "Dadra & Nagar Haveli And Daman & Diu": "U04"}

    base_url = "https://results.eci.gov.in/" + url + dict[state] + ".htm?st=" + dict[state]
    response = requests.get(base_url)
    html = response.content

    soup = BeautifulSoup(html)

    vote = soup.find_all('script', type='text/javascript')

    text = vote[2].string
    text = text.split(';')
    text = text[8].strip()
    text = text.replace('[', ' ')
    text = text.replace('(', '')
    text = text.replace('{', ' ')
    text = text.replace('}', ' ')
    text = text.replace(']', ' ')
    text = text.replace(')', '')
    text = text.replace("'", ' ')
    text = text.replace(",", ' ')
    text = text.replace('%',"")
    text = text.split()
    text = text[1:]

    lst = []
    for i in range(0, len(text), 3):
        lst.append(text[i:i + 3])

    data = pd.DataFrame(lst, columns=["Party", 'Vote Percentage', 'Votes'])
    data[['Vote Percentage', 'Votes']] = data[['Vote Percentage', 'Votes']].apply(pd.to_numeric)
    data.index+=1
    return (data)


#this function returns list of states in selected state
def state_names(url):
    base_url = "https://results.eci.gov.in/"+url
    response = requests.get(base_url)

    html = response.content

    soup = BeautifulSoup(html,'lxml')


    select = soup.find_all('select')



    s = select[0].find_all('option')


    state=[]
    for i in range(0,len(s)):
        state.append(s[i].text)

    return(state)




#This function returns dict of constituency and their number
def constituencies_dict(url,state):
    dict = {"Andhra Pradesh":"S01","Assam":"S03","Bihar":"S04","Goa":"S05","Haryana":"S07","Himachal Pradesh":"S08","Karnataka":"S10","Madhya Pradesh":"S12","Maharashtra":"S13","Manipur":"S14","Meghalaya":"S15","Mizoram":"S16","Nagaland":"S17","Punjab":"S19","Rajasthan":"S20","Uttar Pradesh":"S24","Uttarakhand":"S28","Telangana":"S29","West Bengal":"S25","Dadra & Nagar Haveli And Daman & Diu":"U04"}

    base_url='https://results.eci.gov.in/'+url[0:(url.index('/')+1)]+'Constituencywise'+dict[state]+'1.htm?ac=1'
    response = requests.get(base_url)
    html = response.content

    soup = BeautifulSoup(html,'lxml')


    input_id = soup.find_all('input',id=dict[state])


    txt= str(input_id[0])


    start=txt.index('value=')+7

    txt=txt[start:-3]


    txt = txt.replace(' ',"")

    txt=txt.replace(',',' ')



    txt= txt.replace(';',' ')
    lst=txt.split()


    dict={}
    for i in range(0,len(lst),2):
        dict[lst[i+1]]=lst[i]
    return(dict)




#this function returns candidate wise result
def candidate_wise_result(url,state,constituency):
    dict = {"Andhra Pradesh":"S01","Assam":"S03","Bihar":"S04","Goa":"S05","Haryana":"S07","Himachal Pradesh":"S08","Karnataka":"S10","Madhya Pradesh":"S12","Maharashtra":"S13","Manipur":"S14","Meghalaya":"S15","Mizoram":"S16","Nagaland":"S17","Punjab":"S19","Rajasthan":"S20","Uttar Pradesh":"S24","Uttarakhand":"S28","Telangana":"S29","West Bengal":"S25","Dadra & Nagar Haveli And Daman & Diu":"U04"}
    base_url = 'https://results.eci.gov.in/'+url[0:(url.index('/')+1)]+'Constituencywise'+dict[state]+""+constituency+'.htm?ac='+constituency
    response = requests.get(base_url)
    html= response.content
    soup = BeautifulSoup(html,'lxml')
    table = soup.find_all('table')
    table[0]

    th = table[0].find_all('th')
    heading=[]
    for i in range(0,len(th)):
        heading.append(th[i].text)

    table[0]

    tr = table[0].find_all('tr',style="font-size:12px;")
    tr

    len(tr)

    rows=[]
    for i in range(0,len(tr)):
        td = tr[i].find_all('td')
        for j in range(0,len(td)):
            rows.append(td[j].text)


    d={}
    j=1
    for i in range(0,len(rows),7):
        d[j]=rows[i:i+8]
        j+=1
    heading.append('hello')
    data=pd.DataFrame.from_dict(d,orient='index',columns=heading)
    data.drop(['O.S.N.','hello'],axis=1,inplace=True)
    return(data)



