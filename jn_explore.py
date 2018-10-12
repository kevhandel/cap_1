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
        fate_list.extend(df.columns[39:105])
        df3 = df.filter(fate_list)
        print(year)
    df3.to_csv(full_path)
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
    path = file_path = '~/galvanize/capstone/1_cap/data/'
    chems_file = 'chems.csv'
    chems = ['BENZENE', 'CREOSOTE', 'POLYCHLORINATED BIPHENYLS']
    ac_file = '__all_chemical_names.csv'
    small_fates = ['5.1_FUGITIVE_AIR'] # p=5-7
    small_fates = ['5.2_STACK_AIR'] # p=2-7
    small_fates = ['5.3_WATER'] # p=1-6

    # p = multiprocessing.Process(target=create_all_chems, args=(file_path, chems_file))
    # print(p)
    # p.start()
    all_chemicals = get_chem_names(file_path, ac_file)
    # create_single_chem(file_path, chems_file, all_chemicals)
    # print('all: ', all_chemicals)
    power = 3
    is_small_chems = 1
    is_small_fates = 1
    df_fates = get_one_chem(file_path, 'BENZENE')
    fates = df_fates.columns[list(df_fates.columns).index('5.1_FUGITIVE_AIR'):-2]

    if is_small_chems:
        all_chemicals = chems
    if is_small_fates:
        fates = small_fates

    min_emit = 10**power
    inner_dict = {}
    fate_dict = {}
#    df_fates = get_one_chem(file_path, 'BENZENE')
#    fates = df_fates.columns[list(df_fates.columns).index('5.1_FUGITIVE_AIR'):-2]
    for x, chem in enumerate(all_chemicals):
        x_chem = x
        df_test = get_one_chem(file_path, chem)
        for i, fate in enumerate(fates[0:len(fates)]):
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

    chem = 'CREOSOTE'
    fate = 'small_fates[0]'
    fate = '5.1_FUGITIVE_AIR'
    all_chemicals = get_chem_names(path, ac_file)
    pounds_left = []
    pounds_right = []
    for x, chem in enumerate(all_chemicals[0:100]):
        df_new = get_one_chem(path, chem)
        if df_new.empty:
            continue
        df_left = df_new[df_new['YEAR']<2003]
        df_right = df_new[df_new['YEAR']>=2003]
        dS_left = df_left[df_left[fate]>0].groupby('YEAR').sum()
        pounds_left.extend(list(dS_left[fate]))
        dS_right = df_right[df_right[fate]>0].groupby('YEAR').sum()
        pounds_right.extend(list(dS_right[fate]))
        p_left = [x for x in pounds_left if x > .1*max(pounds_left) and x < .9*max(pounds_left)]
        p_right = [x for x in pounds_right if x > .1*max(pounds_right) and x < .9*max(pounds_right)]
'''next create histogram plotting routine for these left & right distributions'''

# df_benzene = df_chems[df_chems['CHEMICAL']=='BENZENE']
# df_creosote = df_chems[df_chems['CHEMICAL']=='CREOSOTE']
# df_pcb = df_chems[df_chems['CHEMICAL']=='POLYCHLORINATED BIPHENYLS']
print("done done")
'''
fates = ['5.1_FUGITIVE_AIR', '5.2_STACK_AIR', '5.3_WATER', '5.4_UNDERGROUND',
       '5.4.1_UNDERGROUND_CLASS_I', '5.4.2_UNDERGROUND_CLASS_II-V',
       '5.5.1_LANDFILLS', '5.5.1A_RCRA_C_LANDFILLS', '5.5.1B_OTHER_LANDFILLS',
       '5.5.2_LAND_TREATMENT', '5.5.3_SURFACE_IMPOUNDMENT',
       '5.5.3A_RCRA_C_SURFACE_IMP.', '5.5.3B_Other_SURFACE_IMP.',
       '5.5.4_OTHER_DISPOSAL', 'ON-SITE_RELEASE_TOTAL',
       '6.1_POTW-TRANSFERS_FOR_RELEASE', '6.1_POTW-TRANSFERS_FOR_TREATM.',
       '6.1_POTW-TOTAL_TRANSFERS', '6.2_M10', '6.2_M41', '6.2_M62', '6.2_M71',
       '6.2_M81', '6.2_M82', '6.2_M72', '6.2_M63', '6.2_M66', '6.2_M67',
       '6.2_M64', '6.2_M65', '6.2_M73', '6.2_M79', '6.2_M90', '6.2_M94',
       '6.2_M99', 'OFF-SITE_RELEASE_TOTAL', '6.2_M20', '6.2_M24', '6.2_M26',
       '6.2_M28', '6.2_M93', 'OFF-SITE_RECYCLED_TOTAL', '6.2_M56', '6.2_M92',
       'OFF-SITE_RECOVERY_TOTAL', '6.2_M40', '6.2_M50', '6.2_M54', '6.2_M61',
       '6.2_M69', '6.2_M95', 'OFF-SITE_TREATED_TOTAL', 'TOTAL_RELEASES',
       '8.1_RELEASES', '8.1A_ON-SITE_CONTAINED_REL.',
       '8.1B_ON-SITE_OTHER_RELEASES', '8.1C_OFF-SITE_CONTAINED_REL.',
       '8.1D_OFF-SITE_OTHER_RELEASES', '8.2_ENERGY_RECOVERY_ON-SITE',
       '8.3_ENERGY_RECOVERY_OFF-SITE', '8.4_RECYCLING_ON-SITE',
       ' 8.5_RECYCLING_OFF-SITE', '8.6_TREATMENT_ON-SITE',
       '8.7_TREATMENT_OFF-SITE', 'PROD._WASTE_(8.1_THRU_8.7)']
'''
