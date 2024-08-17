import matplotlib.pyplot as plt
from collections import Counter



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



