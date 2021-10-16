import pandas as pd

"""Get the list of university ID"""
#df = pd.read_csv('University List - 4 Year Private - Not for Profit.csv')
#college_id = df['unitid']
#list = list(college_id)

"""Get the empty list of schools"""
#df2 = pd.read_csv('1. Grand total (EF2019  All students  Undergraduate  Degree:certificate-seeking  First-time).csv')
#empty = df2[df2['Grand total (EF2019  All students  Undergraduate  Degree/certificate-seeking  First-time)'].isna()]
#empty = empty[['UnitID', 'Institution Name']]
#empty.to_csv('college_missing_data.csv')

df1 = pd.read_csv('1. Grand total (EF2019  All students  Undergraduate  Degree:certificate-seeking  First-time).csv')
df1.dropna(subset = ['Grand total (EF2019  All students  Undergraduate  Degree/certificate-seeking  First-time)'], inplace=True)
df1 = (df1.set_index(["UnitID", "Institution Name"])
         .stack()
         .reset_index(name='1 Value')
         .rename(columns={'level_2':'1'}))

df2 = pd.read_csv('2. Full-time adjusted fall cohort from prior year.csv')
df2.dropna(subset = ['Full-time adjusted fall 2018 cohort (EF2019D)'], inplace=True)
df2 = (df2.set_index(["UnitID", "Institution Name"])
         .stack()
         .reset_index(name='2 Value')
         .rename(columns={'level_2':'2'}))

df3 = pd.read_csv('3. Students from prior year\'s adjusted full-time fall cohort enrolled in current year.csv')
df3.dropna(subset = ['Students from the full-time adjusted fall 2018 cohort enrolled in fall 2019 (EF2019D)'], inplace=True)
df3 = (df3.set_index(["UnitID", "Institution Name"])
         .stack()
         .reset_index(name='3 Value')
         .rename(columns={'level_2':'3'}))

df23 = pd.concat([df2, df3], axis=1, join='inner')
df23 = df23[['UnitID', 'Institution Name', '2', '2 Value', '3', '3 Value']]
df23['Retention'] = df23['3 Value'] / df23['2 Value']

df123 = pd.concat([df1, df23], axis=1, join='inner')
df123 = df123[['UnitID', 'Institution Name', '1', '1 Value', '2', '2 Value', '3', '3 Value', 'Retention']]


df123 = df123.loc[:,~df123.columns.duplicated()]