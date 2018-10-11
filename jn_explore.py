import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import date
from datetime import time
import multiprocessing

#%matplotlib inline
import csv

def set_date():
    pd.set_option('display.max_columns', 110)
    today = date.today()
    days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    now = datetime.now()
    md = f'{today.day}_{today.month}_{days[today.weekday()]}_{now.microsecond}'

def create_plot():
    df_chems = pd.read_csv('~/galvanize/capstone/1_cap/data/unique_chems.csv')
    fig, ax = plt.subplots()
    ax.plot(df_chems['Year'], df_chems['Unique_chemical'])
    #rotate and align the tick labels so they look better
    fig.autofmt_xdate()
    ax.set_title('Unique Chemicals Inventoried in \n US EPA TRI by Year')
    plt.savefig(f'figs/chemsicals_{md}.png')
    plt.show()

def create_all_chems(path, file):
    full_path = path+file
    df2 = df = pd.DataFrame()
    print('Year', 'Unique Chemicals')
    for year in range(1987, 2017):
        df2 = pd.read_csv('~/galvanize/capstone/1_cap/data/TRI_/TRI_'+str(year)+'_US.csv', low_memory=False)
        df = df.append(df2)
        fate_list = ['CHEMICAL', 'YEAR']
        fate_list.extend(df.columns[39:106])
        df3 = df.filter(fate_list)
        print(year)
    # df3.to_csv(full_path)
    all_chemicals = df3['CHEMICAL'].unique()
    return(all_chemicals)

def create_single_chem(path, file, names):
    print('creating single chems...')
    chems_file = path + file
    df = pd.read_csv(chems_file, low_memory=False)
    for name in names:
        df_one = df[df['CHEMICAL']==name]
        full_path = path+'_'+name.replace(' ','_').lower()+'.csv'
        df_one.to_csv(full_path)# chems_file = path + file
        print(f'{name} file now exists')
    all_chemicals = df['CHEMICAL'].unique()
    return all_chemicals

def get_one_chem(path, name):
    file_path = path+'_'+name.replace(' ', '_').lower()+'.csv'
    df = pd.read_csv(file_path, low_memory=False)
    return df

def create_year_plot(series, title_chem_fate_yaxis):
    tcfy = title_chem_fate_yaxis
    fig, ax = plt.subplots()
    ax.plot(series)
    #rotate and align the tick labels so they look better
    fig.autofmt_xdate()
    ax.set_title(title_chem_fate_yaxis[0])
    ax.set_ylabel(tcfy[3])
    plt.savefig(f'figs/fig_chemicals_{tcfy[1].replace(" ", "_")}_{tcfy[2].replace(" ", "_")}.png')
#    plt.show()

def get_chem_names(path, name):
    file_path = path + name
    df = pd.read_csv(file_path, low_memory=False)
    return df['CHEMICAL'].unique()

if __name__ == '__main__':
    file_path = '~/galvanize/capstone/1_cap/data/'
    chems_file = 'chems.csv'
    chems = ['BENZENE', 'CREOSOTE', 'POLYCHLORINATED BIPHENYLS']
   # p = multiprocessing.Process(target=create_all_chems, args=(file_path, chems_file))
   # print(p)
   # p.start()
    all_chemicals = get_chem_names(file_path, chems_file)
#    create_single_chem(file_path, chems_file, all_chemicals)
    # print('all: ', all_chemicals)
    power = 7
    is_small_sample = 1
    if is_small_sample:
        all_chemicals = chems
    min_emit = 10**power
    inner_dict = {}
    fate_dict = {}
    df_fates = get_one_chem(file_path, 'BENZENE')
    fates = df_fates.columns[list(df_fates.columns).index('5.1_FUGITIVE_AIR'):-2]
    for x, chem in enumerate(all_chemicals):
        x_chem = x
        df_test = get_one_chem(file_path, chem)
        for i, fate in enumerate(fates[0:len(fates)-2]):
            fate_series = df_test.groupby("YEAR")[fate]
            title = f'Yearly Emissions of {chem}\nby {fate}'
            yaxis = 'Pounds'
            t_c_f_y = [title, chem, fate, yaxis]
            fsum_mean = np.mean(list(fate_series.sum()))
            if fsum_mean > min_emit:
                inner_dict[fate] = [fate_series.sum(), t_c_f_y]
                create_year_plot(fate_series.sum(), t_c_f_y)
        if bool(inner_dict):
            fate_dict[chem] = inner_dict
            inner_dict = {}

# df_benzene = df_chems[df_chems['CHEMICAL']=='BENZENE']
# df_creosote = df_chems[df_chems['CHEMICAL']=='CREOSOTE']
# df_pcb = df_chems[df_chems['CHEMICAL']=='POLYCHLORINATED BIPHENYLS']
print("done done")
