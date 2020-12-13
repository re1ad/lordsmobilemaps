import csv
from time import sleep
import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent


def write_csv(data):
    with open('data.csv', 'a', encoding='utf-8') as file:
        order = [
            '#',
            'Kingdom Name',
            'Population',
            'Best power clan name',
            'Best kills clan name',
            'Best power player name',
            'Best kills player name'
        ]
        writer = csv.DictWriter(file, fieldnames=order, delimiter=',', lineterminator='\n')
        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(data)


def get_html(url):
    sleep(1)
    headers = {
        'Accept': '*/*',
        'User-Agent': generate_user_agent()
    }
    response = requests.get(url, headers=headers)
    return response.text


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('div', class_='toptab toptab3').find_all('div', class_='toptabrow')
    if not table:
        raise ValueError
    for element in table:
        try:
            num = element.select_one('div:nth-child(1)').text.strip()
        except:
            num = ''
        try:
            kingdom_name = element.select_one('div:nth-child(2) > a').text.strip()
        except:
            kingdom_name = ''
        try:
            population = element.select_one('div:nth-child(3)').text.strip()
        except:
            population = ''
        try:
            best_power_clan_name = element.select_one('div:nth-child(4) > a').text.strip()
        except:
            best_power_clan_name = ''
        try:
            best_kills_clan_name = element.select_one('div:nth-child(5) > a').text.strip()
        except:
            best_kills_clan_name = ''
        try:
            best_power_player_name = element.select_one('div:nth-child(6) > a').text.strip()
        except:
            best_power_player_name = ''
        try:
            best_kills_player_name = element.select_one('div:nth-child(7) > a').text.strip()
        except:
            best_kills_player_name = ''

        data = {
            '#': num,
            'Kingdom Name': kingdom_name,
            'Population': population,
            'Best power clan name': best_power_clan_name,
            'Best kills clan name': best_kills_clan_name,
            'Best power player name': best_power_player_name,
            'Best kills player name': best_kills_player_name
        }
        write_csv(data)


def main():
    pattern = 'https://lordsmobilemaps.com/en/kingdom/ranking/population/{}'
    paginate = 1
    while True:
        url = pattern.format(str(paginate))
        try:
            get_page_data(get_html(url))
            paginate += 1
        except ValueError:
            break


if __name__ == '__main__':
    main()
