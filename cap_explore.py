import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib inline
import csv

years = []
chems = []
df_chems = pd.read_csv('~/galvanize/capstone/data/unique_chems.csv')
#df_chems.plot.bar(x='Year', y='Unique_chemical', rot=0)
fig, ax = plt.subplots()
ax.plot(df_chems['Year'], df_chems['Unique_chemical'])
# rotate and align the tick labels so they look better
fig.autofmt_xdate()
ax.set_title('Unique Chemicals Inventoried in \n US EPA TRI by Year')

plt.savefig('data/chems.png')
#plt.show()

# print('Year', 'Unique Chemicals')
# for year in range(1987, 2017):
#     df = pd.read_csv('~/galvanize/capstone/data/TRI_'+str(year)+'_US.csv', low_memory=False)
#     counts = df.CHEMICAL.unique().size
#     print(year, counts)
#     years.append(int(year))
#     chems.append(counts)

# with open('unique_chems.csv', mode='w') as chem_file:
#     f_writer = csv.writer(chem_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     f_writer.writerow(['Year', 'Unique_chemical'])
#     for year, chem in zip(years, chems):
#         f_writer.writerow([year, chem])
