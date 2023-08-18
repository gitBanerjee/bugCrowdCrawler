# Created By Sourav Banerjee
import requests
import html
from bs4 import BeautifulSoup
import re
import time


# Controls
base_url = 'https://bugcrowd.com'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
time_param = 0.3
dead_programs = []
stats_param = 100
sorting = 'promoted-desc'
searchAllPages = True if input("Do you want to search in all the pages? (y/n): ").lower() == "y" else False

def checkUserRank(href_value, response):
     user_url = base_url + href_value
     user_response = requests.get(user_url, headers=headers)
     if response.status_code == 200:
        stat_pattern = r',"rank":"(\d+)'
        stats = re.findall(stat_pattern, html.unescape(user_response.text))
        # making 0 as high end user and 1 as low end one
        if len(stats) > 0 and int(stats[0]) < stats_param:
            return 0
        else:
            return 1
        
def getAllPrograms():
    all_programs = []
    total_pages = 1
    api_url = base_url + '/programs.json'

    api_response = requests.get(api_url, headers=headers)
    json_data = api_response.json()
    print('Trying to fetch all the programs, this may take some time...')

    if searchAllPages and api_response.status_code == 200:
        total_pages = json_data['meta']['totalPages']

    for page_number in range(1, total_pages + 1):
        time.sleep(time_param)
        api_response = requests.get(f"{api_url}?sort[]={sorting}&page[]={page_number}", headers=headers)
        json_data = api_response.json()
        if api_response.status_code == 200:
            program_json = json_data['programs']
            for program in program_json:
                program_url = program['program_url']
                all_programs.append(program_url)
        else:
            print(f"Failed to fetch data for page {page_number}. Status code: {api_url.status_code}")
    return all_programs

def main():
    url = base_url + '/programs'
    response = requests.get(url, headers=headers)
    all_programs = getAllPrograms()
    print(all_programs)

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
                decision_param = checkUserRank(href_value, response)
                if decision_param == 0:
                    print('Leaving program ' + program.replace('/', '') + ' as it has a user ' + href_value.replace('/', '') + ' with a rank under ' + str(stats_param))
                    dead_programs.append(program)
                    break
        else:
            print(f"Failed to fetch data from: {hall_of_fame_url}")

    programs_to_enlist = [x for x in all_programs if x not in dead_programs]
    print(programs_to_enlist)

if __name__ == "__main__":
    main()
