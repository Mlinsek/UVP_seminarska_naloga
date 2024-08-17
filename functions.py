import re
from bs4 import BeautifulSoup
import pandas as pd

html_1 = r"C:\Users\marti\OneDrive\Namizje\UVP_seminarska_naloga\100 metres - Wikipedia.html"
html_2 = r"C:\Users\marti\OneDrive\Namizje\UVP_seminarska_naloga\100 Metres - men - senior - all.html"

def wr_times_date_nationalities_function(file, x):
    with open(file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    wr_times = []

    for row in soup.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) > 0:
            time_str = columns[x].get_text(strip=True)
            wr_times.append(time_str)
            
    return wr_times


# funkcija prebere HTML datoteko
# s pomočjo knjižnice BeautifulSoup poišče vse vrstice tabele (`<tr>`) 
# iz vsake vrstice prebere (`<td>`), vsakic se v tabeli vziramo na drugo mesto  
# čase shrani v seznam `wr_times`... in ga na koncu vrne

# s pomočjo te funkcije lahko iz ene tabele izluščimo veliko podatkov

def reaction_times_function(file):
    with open(file, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')
    reaction_times = []
    for table in soup.find_all('table', class_='wikitable'):
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if cells:
                for cell in cells:
                    text = cell.get_text(strip=True)
                    match = re.match(r'^0\.\d{3}$', text)
                    if match:
                        reaction_times.append(text)
    
    return reaction_times

# funkcija prebere HTML datoteko in s pomočjo BeautifulSoup poišče vse tabele z razredom 'wikitable'
# znotraj teh tabel iz vsake vrstice poišče reakcijske čase v obliki '0.xxx' s pomočjo regularnega izraza
# čase shrani v seznam, nato ga vrne


def wind_speed_function(file):
    with open(file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    wind_speed_pattern = r'[\+\-][0-1]\.\d|[\+\-]2\.0'
    wind_speeds = re.findall(wind_speed_pattern, text)
    data_frame_wind_speeds = pd.DataFrame(wind_speeds, columns=['Wind Speed'])
    wind_speed = data_frame_wind_speeds['Wind Speed'].tolist()
    
    return wind_speed

# funkcija prebere HTML datoteko in s pomočjo BeautifulSoup pridobi tekst
# iz besedi izlušči hitrosti vetra v območju med -2.0 in +2.0 
# hitrosti shrani v Dataframe


wr_times = wr_times_date_nationalities_function(html_2, 1)
date_of_birth = wr_times_date_nationalities_function(html_2, 4)
nationalities = wr_times_date_nationalities_function(html_2, 5)
athlets = wr_times_date_nationalities_function(html_2, 3)
wind_speed = wind_speed_function(html_1)
wind = wr_times_date_nationalities_function(html_2, 2)
reaction_times = reaction_times_function(html_1)

