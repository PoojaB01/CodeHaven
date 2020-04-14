from bs4 import *
import requests
import re
from datetime import date
import time
import datetime
import json
from math import *

def expectedRank(arr,r):
    seed = 1
    for i in arr:
        seed = seed + 1/(1+10**((r-i)/400))
    return seed

def b_search(arr,seed):
    start = 0 
    end = 4000
    while start<end:
        mid = (start + end)/2
        E_R = expectedRank(arr,mid)
        if abs(E_R-seed) < 5:
            return mid
        if E_R > seed :
            start = mid + 1
        else:
             end = mid + 1
    return 0

def crawler_1(user, contest_code, question_code):

    u =  'https://codeforces.com/api/contest.status?contestId='+contest_code+'&handle='+user

    r = requests.get(u)

    data = r.json()
    data = data['result']

    for submission in data:
        if submission['problem']['index']==question_code and submission['verdict']=='OK':
            u = 'https://codeforces.com/contest/'+contest_code+'/submission/'+str(submission['id'])
            code_page = requests.get(u).text
            soup_code = BeautifulSoup(code_page, 'lxml')
            return soup_code.find("pre", id="program-source-text").stripped_strings
    


def crawler_2(user):
    u = "https://codeforces.com/api/user.info?handles="+user
    r = requests.get(u)
    data = r.json()
    data = data['result'][0]
    result={}
    result['handle'] = user
    result['name'] = ''
    if 'firstName' in data:
        result['name'] = data['firstName']
    if 'lastName' in data:
        result['name'] = result['name'] + ' ' + data['lastName']
    if 'rating' in data:
        result['rating'] = data['rating']
        result['maxRating'] = data['maxRating']
        result['maxRank'] = data['maxRank']
        result['rank'] = data['rank']
        u = "https://codeforces.com/api/user.rating?handle="+user
        r = requests.get(u)
        data = r.json()
        data = data['result']
        #print(data)
        i1 = 0
        i2 = 0
        min_change = data[0]['newRating'] - data[0]['oldRating']
        max_change = data[0]['newRating'] - data[0]['oldRating']
        best_rank = data[0]['rank']
        min = data[0]['newRating']
        for i in range(len(data)):
            if data[i]['newRating'] < min:
                min=data[i]['newRating']
            if data[i]['newRating'] - data[i]['oldRating' ] > max_change:
                max_change = data[i]['newRating'] - data[i]['oldRating']
                i1 = i
            if data[i]['newRating'] - data[i]['oldRating' ] < min_change:
                min_change = data[i]['newRating'] - data[i]['oldRating']
                i2 = i
            if data[i]['rank'] < best_rank:
                best_rank = data[i]['rank']
        result['max_change'] = { 'change' : max_change , 'name' : data[i1]['contestName'] , 'code' : 'https://codeforces.com/contest/' + str(data[i1]['contestId']) , 'rank' : data[i1]['rank'] , 'oldR' : data[i1]['oldRating'] , 'newR' : data[i1]['newRating'] }
        i1=i2
        result['min_change'] = { 'change' : min_change , 'name' : data[i1]['contestName'] , 'code' : 'https://codeforces.com/contest/' + str(data[i1]['contestId']) , 'rank' : data[i1]['rank'] , 'oldR' : data[i1]['oldRating'] , 'newR' : data[i1]['newRating'] }
        result['best_rank'] = best_rank
        result['contests'] = len(data)
    else:
        result['rating']=-1
    cf_api = requests.get('https://codeforces.com/api/user.status?handle=' + user)
    sub_json = cf_api.json()
    data = sub_json['result']
    if len(data) > 0:
        d0 = date.fromtimestamp(data[len(data)-1]['creationTimeSeconds'])
        d1 = date.today()
        delta = d1 - d0
        result['average_sub'] = len(data)/delta.days*7
    return result




def crawler_3(user):
    codeforces = 'http://codeforces.com/'
    submissions = 'submissions/'
    submissions_page = requests.get(codeforces + submissions + user + "/page/1").text
    soup = BeautifulSoup(submissions_page, 'lxml')
    page_list = soup.find_all("span", class_="page-index")
    page_list = page_list[len(page_list) - 1].find("a").contents
    pages = int(page_list[0])
    attempts = {}
    for page_index in range(1, pages + 1):
        submissions_page = requests.get(codeforces + submissions + user + "/page/" + str(page_index)).text
        soup = BeautifulSoup(submissions_page, 'lxml')
        submissions_table = soup.find_all("table", class_="status-frame-datatable")
        for table_row in submissions_table[0].find_all("tr"):
            for table_data in table_row.find_all("td", class_="status-small"):
                if (table_data.a != None):
                    problem = table_data.a.get("href")
                    problem = " ".join(problem.split("/"))
                    if problem not in attempts:
                        attempts[problem] = 1
                    else:
                        attempts[problem] += 1
    return attempts

def crawler_4(user):
    codeforces = 'https://www.codeforces.com/'
    contests = 'contests/'
    user_page = requests.get(codeforces + contests + 'with/' + user).text
    soup = BeautifulSoup(user_page, 'lxml')
    contest_table = soup.find_all("table", class_="tablesorter user-contests-table")
    contests_dict = {}
    for table_row in contest_table[0].tbody.find_all("tr"):
        if (table_row.a != None):
            contests_dict[table_row.a.get('href')] = 1
    contest_page = requests.get(codeforces + contests).text
    soup_contests = BeautifulSoup(contest_page, 'lxml')
    contest_table = soup_contests.find_all("table", class_="")
    past_contests = contest_table[1]
    contest_date_and_time = {}
    for table_row in past_contests.find_all("tr"):
        if (table_row.a != None):
            time_of_contest = table_row.find_all("span", class_="format-date")
            if (str(table_row.a.get('href')) in contests_dict):
                contest_date_and_time[table_row.a.get('href')] = time_of_contest[0].string
    months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
              'Nov': 11, 'Dec': 12}
    dates_of_contests = []
    for x in contest_date_and_time:
        dates = str(contest_date_and_time[x])
        month = months[dates[:3]]
        day = int(dates[4:6])
        year = int(dates[7:11])
        d = date(year, month, day)
        dates_of_contests.append(d)
    avg_contest_gap = 0
    for i in range(1, len(dates_of_contests) - 1):
        avg_contest_gap += (dates_of_contests[i - 1] - dates_of_contests[i]).days
    avg_contest_gap /= (len(dates_of_contests) - 1)
    return avg_contest_gap


def crawler_5(user1, user2, contest_code):
    codeforces = 'https://www.codeforces.com/'
    contest_page = requests.get(codeforces + 'contest/' + contest_code).text
    soup = BeautifulSoup(contest_page, 'lxml')
    problems_table = soup.find("table", class_="problems")
    problems = {}
    for table_row in problems_table.find_all("tr"):
        table_data = list(table_row.find_all("td"))
        if (len(table_data) > 2):
            code = table_data[0].a.string.strip()
            problems[code] = {}
            problems[code]['name'] = table_data[1].a.get_text()
            problems[code]['attempts1'] = 0
            problems[code]['attempts2'] = 0
            problems[code]['success1'] = 0
            problems[code]['success2'] = 0
            problems[code]['time1'] = 0
            problems[code]['time2'] = 0
    contest_page1 = requests.get(codeforces + 'submissions/' + user1 + '/contest/' + contest_code).text
    contest_page2 = requests.get(codeforces + 'submissions/' + user2 + '/contest/' + contest_code).text
    soup1 = BeautifulSoup(contest_page1, 'lxml')
    soup2 = BeautifulSoup(contest_page2, 'lxml')
    contests_table1 = soup1.find("table" , class_="status-frame-datatable")
    contests_table2 = soup2.find("table", class_="status-frame-datatable")
    for table_row in contests_table1.find_all("tr"):
        table_data = table_row.find_all("td")
        if (len(table_data) > 0):
            code = list(table_data[3].a.get("href").split('/'))[-1]
            problems[code]['attempts1'] += 1
            if (table_data[5].span['submissionverdict'] == 'OK'):
                problems[code]['success1'] += 1
                problems[code]['time1'] = table_data[1].get_text().strip()
    for table_row in contests_table2.find_all("tr"):
        table_data = table_row.find_all("td")
        if (len(table_data) > 0):
            code = list(table_data[3].a.get("href").split('/'))[-1]
            problems[code]['attempts2'] += 1
            if (table_data[5].span['submissionverdict'] == 'OK'):
                problems[code]['success2'] += 1
                problems[code]['time2'] = table_data[1].get_text().strip()
    for A in problems:
        print(A, problems[A]['name'])
        print(user1, problems[A]['attempts1'], problems[A]['success1'], problems[A]['time1'])
        print(user2, problems[A]['attempts2'], problems[A]['success2'], problems[A]['time2'])
    return problems
   
def generate_heat_map(user):
    cf_api = requests.get('https://codeforces.com/api/user.status?handle=' + user)

    sub_json = cf_api.json()

    submissions = {}
    ref = datetime.date(2019, 1, 1)
    for t in sub_json["result"]:
        x = datetime.datetime.fromtimestamp(t["creationTimeSeconds"]).date()
        x = (x - ref).days
        if submissions.get(x) is None:
            submissions[x] = 1
        else:
            submissions[x] = submissions[x] + 1
    return submissions

def generate_pie_chart(user):
    cf_api = requests.get('https://codeforces.com/api/user.status?handle=' + user)
    sub_json = cf_api.json()
    tags = {}
    for keys in sub_json["result"]:
        for tag in keys["problem"]["tags"]:
            if tags.get(tag) is None:
                tags[tag] = 1
            else:
                tags[tag] += 1
    return tags

def crawler_6():
    cf_api = requests.get('https://codeforces.com/api/contest.list')
    contests = cf_api.json()['result']
    upcoming = []
    ongoing = []
    finished = []
    for data in contests:
        if data['phase'] == 'BEFORE':
            new = {}
            new['site'] = 'Codeforces'
            new['link'] = 'https://codeforces.com/contests/' + str(data['id'])
            new['name'] = data['name']
            new['startTime'] = data['startTimeSeconds']
            new['endTime'] = data['durationSeconds'] + data['startTimeSeconds']
            timestamp = datetime.datetime.fromtimestamp(new['startTime'])
            new['startTime'] = timestamp.strftime('%d/%m/%Y %H:%M:%S')
            timestamp = datetime.datetime.fromtimestamp(new['endTime'])
            new['endTime'] = timestamp.strftime('%d/%m/%Y %H:%M:%S')
            upcoming.append(new)
        if data['phase'] == 'CODING':
            new = {}
            new['site'] = 'Codeforces'
            new['link'] = 'https://codeforces.com/contests/' + str(data['id'])
            new['name'] = data['name']
            new['startTime'] = data['startTimeSeconds']
            new['endTime'] = data['durationSeconds'] + data['startTimeSeconds']
            timestamp = datetime.datetime.fromtimestamp(new['startTime'])
            new['startTime'] = timestamp.strftime('%d/%m/%Y %H:%M:%S')
            timestamp = datetime.datetime.fromtimestamp(new['endTime'])
            new['endTime'] = timestamp.strftime('%d/%m/%Y %H:%M:%S')
            ongoing.append(new)
        if data['phase'] == 'FINISHED':
            new = {}
            new['link'] = 'https://codeforces.com/contests/' + str(data['id'])
            new['site'] = 'Codeforces'
            new['name'] = data['name']
            new['startTime'] = data['startTimeSeconds']
            new['endTime'] = data['durationSeconds'] + data['startTimeSeconds']
            timestamp = datetime.datetime.fromtimestamp(new['startTime'])
            new['startTime'] = timestamp.strftime('%d/%m/%Y %H:%M:%S')
            timestamp = datetime.datetime.fromtimestamp(new['endTime'])
            new['endTime'] = timestamp.strftime('%d/%m/%Y %H:%M:%S')
            finished.append(new)
        """
    contests_page = requests.get('https://www.codechef.com/contests').text
    soup = BeautifulSoup(contests_page,'lxml')
    tables = soup.find_all('table', class_='dataTable')
    for j in range(3):
        contest = tables[j].find_all('td')
        for i in range(int(len(contest)/4)):
            new={}
            new['site'] = 'CodeChef'
            new['link'] = 'https://www.codechef.com/' + contest[i*4].get_text()
            #print(new['link'])
            new['name'] = contest[4*i+1].get_text()
            ds = contest[i*4+2].get_text()
            dt = datetime.datetime.strptime(ds, '%d %b %Y %H:%M:%S')
            new['startTime'] = int(time.mktime(dt.timetuple()))
            ds = contest[i*4+3].get_text()
            dt = datetime.datetime.strptime(ds, '%d %b %Y %H:%M:%S')
            new['endTime'] = int(time.mktime(dt.timetuple()))
            timestamp = datetime.datetime.fromtimestamp(new['startTime'])
            new['startTime'] = timestamp.strftime('%d/%m/%Y %H:%M:%S')
            timestamp = datetime.datetime.fromtimestamp(new['endTime'])
            new['endTime'] = timestamp.strftime('%d/%m/%Y %H:%M:%S')
            if j==0:
                ongoing.append(new)
            if j==1:
                upcoming.append(new)
            if j==2:
                finished.append(new) """
    return upcoming , ongoing , finished

def virtual_rating_change(rank,contest_code,rating):
    cf_api = requests.get('https://codeforces.com/api/contest.ratingChanges?contestId='+contest_code)
    oldR_json = cf_api.json()
    oldR_arr = []
    for data in oldR_json['result']:
        oldR_arr.append(data['oldRating'])
    seed = expectedRank(oldR_arr,rating)
    gm_rank = sqrt(seed*rank)
    R_seed = b_search(oldR_arr,gm_rank)
    print(seed,R_seed)
    return int((R_seed-rating)/2)
