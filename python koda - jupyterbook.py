import matplotlib.pyplot as plt
from collections import Counter
import re


from table import full_analysis_information

for athlete in full_analysis_information:
    if isinstance(athlete['Time'], str):  
        athlete['Time'] = float(athlete['Time'].split()[0])

sorted_athletes = sorted(full_analysis_information, key=lambda x: x['Time'])

names = [athlete['Name'] for athlete in sorted_athletes]
times = [athlete['Time'] for athlete in sorted_athletes]

plt.figure(figsize=(12, 6))
plt.barh(names, times, color='skyblue')
plt.xlabel('Čas (v sekundah)')
plt.ylabel('Ime atleta')
plt.title('Časi najboljših šprinterjev na 100m (od najhitrejšega do najpočasnejšega)')
plt.xlim(min(times) - 0.1, max(times) + 0.1)
plt.gca().invert_yaxis()
plt.savefig('wr_times.png')

#--------------------------------------------------------------------------------------------------------------------------

from functions import nationalities

country_counts = Counter(nationalities)
labels = ['USA', 'JAM', 'Other']
sizes = [
    country_counts.get('USA', 0),
    country_counts.get('JAM', 0),
    sum(count for country, count in country_counts.items() if country not in ['USA', 'JAM'])
]

plt.figure(figsize=(10, 6))
plt.pie(sizes, labels=labels, startangle=140, colors=plt.cm.Paired.colors)
plt.axis('equal')
plt.title('Porazdelitev nacionalnosti med šprinterji (samo USA in JAM)')
plt.savefig('tortni_diag.png')

#--------------------------------------------------------------------------------------------------------------------------

def calculate_hypothetical_time(time, reaction_time, wind_speed):
    wind_adjustment = (wind_speed / 2.0) * 0.1
    hypothetical_time = time - reaction_time + wind_adjustment
    return hypothetical_time

names = []
times = []
hypothetical_times = []

for athlete in full_analysis_information:
    names.append(athlete["Name"])
    times.append(athlete["Time"])
    hypothetical_time = calculate_hypothetical_time(athlete["Time"], athlete["Reaction Time"], athlete["Wind Speed"])
    hypothetical_times.append(hypothetical_time)

plt.figure(figsize=(10, 6))
plt.plot(names, times, marker='o', linestyle='-', color='b', label='Dejanski čas')
plt.plot(names, hypothetical_times, marker='o', linestyle='--', color='r', label='Hipotetičen čas (brez reakcije in vetra)')
plt.xlabel("Ime atleta")
plt.ylabel("Čas (v sekundah)")
plt.title("Primerjava dejanskega časa in hipotetičnega časa na 100m")
plt.xticks(rotation=45, ha='right')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('comparison_plot.png')

# predpostavimo: vsakih +2.0 m/s vetra skrajša čas za 0.1 sekunde
# morda vreden komentar, funkcija, ki smo jo zapisali v table.py se izkaže za neuporabno
#--------------------------------------------------------------------------------------------------------------------------

from table import date
from functions import date_of_birth
from table import names

def first_six_elements(input_list):
    return input_list[:6]

date_of_birth_6 = first_six_elements(date_of_birth)
date1 = first_six_elements(date)
names1 = first_six_elements(names)
def extract_xxxx_numbers(list):
    pattern = r'\b\d{4}\b'
    extracted_numbers = []
    
    for item in list:
        match = re.findall(pattern, item)
        extracted_numbers.extend(match)
    
    return extracted_numbers

date_of_birth_6_usable = extract_xxxx_numbers(date_of_birth_6)
date1_usable = extract_xxxx_numbers(date1)

def calculate_ages(birth_years, record_years):
    ages = []
    for birth_year, record_year in zip(birth_years, record_years):
        age = int(record_year) - int(birth_year)
        ages.append(age)
    return ages

ages = calculate_ages(date_of_birth_6_usable, date1_usable)

plt.figure(figsize=(8, 5))
plt.plot(names1, ages, marker='o', linestyle='-', color='b')
plt.xlabel("Athletes")
plt.ylabel("Age at Record (Years)")
plt.title("Age of Athletes When They Set Their Records")
plt.grid(True)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('age_plot.png')

#--------------------------------------------------------------------------------------------------------------------------

average_age = sum(ages) / len(ages)
athlete_data = [[name, age] for name, age in zip(names, ages)]
athlete_data.append(["Average Age", f"{average_age:.2f}"])
fig, ax = plt.subplots(figsize=(8, 6))
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=athlete_data, colLabels=["Name", "Age at Record"], cellLoc='center', loc='center')

table.auto_set_font_size(False)
table.set_fontsize(10)
ax.set_title('Ages of Athletes When They Set Their Records and Average Age', fontsize=12)

plt.savefig('athlete_age_table_with_average.png', bbox_inches='tight', dpi=300)
plt.savefig('age_table.png')

#--------------------------------------------------------------------------------------------------------------------------
