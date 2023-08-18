# Created By Sourav Banerjee
import requests
import html
from bs4 import BeautifulSoup
import re
import time

base_url = 'https://bugcrowd.com'
url = base_url + '/programs'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
time_param = 0.5

response = requests.get(url, headers=headers)
pattern = r'"program_url":"(.*?)"'
all_programs = re.findall(pattern, html.unescape(response.text))
print(all_programs)
dead_programs = []
stats_param = 100

def checkUserRank(href_value):
     user_url = base_url + href_value
     user_response = requests.get(user_url, headers=headers)
     if response.status_code == 200:
        stat_pattern = r',"rank":"(\d+)'
        stats = re.findall(stat_pattern, html.unescape(user_response.text))
        print(stats, href_value)
        # making 0 as high end user and 1 as low end one
        if len(stats) > 0 and int(stats[0]) < stats_param:
            return 0
        else:
            return 1

for program in all_programs:
    hall_of_fame_url = base_url + program + '/hall-of-fame'
    program_response = requests.get(hall_of_fame_url, headers)

    if response.status_code == 200:
        soup = BeautifulSoup(program_response.text, 'html.parser')
        tags= []
        tags = soup.find_all('a', class_='bc-panel bc-panel--interactive', style='width:100%')               #may change time to time
        if not tags:
            tags = soup.find_all('a', class_='bc-userblock')
        for user in tags:
            href_value = user.get('href')
            time.sleep(time_param)
            decision_param = checkUserRank(href_value)
            if decision_param == 0:
                dead_programs.append(program)
                break
    else:
        print(f"Failed to fetch data from: {hall_of_fame_url}")

programs_to_enlist = [x for x in all_programs if x not in dead_programs]
print(programs_to_enlist)
