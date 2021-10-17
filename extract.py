import pandas as pd

"""Get the list of university ID"""
#df = pd.read_csv('University List - 4 Year Private - Not for Profit.csv')
#college_id = df['unitid']
#list = list(college_id)

"""Get the empty list of schools"""
df2 = pd.read_csv('1. Grand total (EF2019  All students  Undergraduate  Degree:certificate-seeking  First-time).csv')
empty = df2[df2['Grand total (EF2019  All students  Undergraduate  Degree/certificate-seeking  First-time)'].isna()]
empty = empty[['UnitID', 'Institution Name']]
empty_id = list(empty['UnitID'])
#empty.to_csv('college_missing_data.csv')

"""df123"""
# Note that Thomas Jefferson only have 2 years record, so we are omitting it as well.

df1 = pd.read_csv('1. Grand total (EF2019  All students  Undergraduate  Degree:certificate-seeking  First-time).csv')
df1.dropna(subset = ['Grand total (EF2012_RV  All students  Undergraduate  Degree/certificate-seeking  First-time)'], inplace=True)
df1 = (df1.set_index(["UnitID", "Institution Name"])
         .stack()
         .reset_index(name='First year Value')
         .rename(columns={'level_2':'First year'}))

df2 = pd.read_csv('2. Full-time adjusted fall cohort from prior year.csv')
df2.dropna(subset = ['Full-time adjusted fall 2011 cohort (EF2012D_RV)'], inplace=True)
df2 = (df2.set_index(["UnitID", "Institution Name"])
         .stack()
         .reset_index(name='2 Value')
         .rename(columns={'level_2':'2'}))

df3 = pd.read_csv('3. Students from prior year\'s adjusted full-time fall cohort enrolled in current year.csv')
df3.dropna(subset = ['Students from the full-time adjusted fall 2011 cohort enrolled in fall 2012 (EF2012D_RV)'], inplace=True)
df3 = (df3.set_index(["UnitID", "Institution Name"])
         .stack()
         .reset_index(name='3 Value')
         .rename(columns={'level_2':'3'}))

df23 = pd.concat([df2, df3], axis=1, join='inner')
df23 = df23[['UnitID', 'Institution Name', '2', '2 Value', '3', '3 Value']]
df23['Retention'] = df23['3 Value'] / df23['2 Value']

df123 = pd.concat([df1, df23], axis=1, join='inner')
df123 = df123[['UnitID', 'Institution Name', 'First year', 'First year Value', '2', '2 Value', '3', '3 Value', 'Retention']]


df123 = df123.loc[:,~df123.columns.duplicated()]

"""df456"""
# Note that Thomas Jefferson only have 2 years record, so we are omitting it as well.

df4 = pd.read_csv('4. Publish in-state tuition and fees.csv')
df4.dropna(subset = ['Published in-state tuition and fees 2012-13 (IC2012_AY)'], inplace=True)
df4 = (df4.set_index(["UnitID", "Institution Name"])
         .stack()
         .reset_index(name='4 Value')
         .rename(columns={'level_2':'4'}))

df5 = pd.read_csv('5. Full time total (EF2019  All students  Undergraduate  Degree:certificate-seeking  First-time).csv')
df5.dropna(subset = ['Full time total (EF2012_RV  All students  Undergraduate  Degree/certificate-seeking  First-time)'], inplace=True)
df5 = (df5.set_index(["UnitID", "Institution Name"])
         .stack()
         .reset_index(name='5 Value')
         .rename(columns={'level_2':'5'}))

df6 = pd.read_csv('6. Total amount of institutional grant aid awarded to full-time first-time undergraduates.csv')
df6.dropna(subset = ['Total amount of institutional grant aid awarded to full-time first-time undergraduates (SFA1213_RV)'], inplace=True)
df6 = (df6.set_index(["UnitID", "Institution Name"])
         .stack()
         .reset_index(name='6 Value')
         .rename(columns={'level_2':'6'}))

df456 = pd.concat([df4, df5, df6], axis=1, join='inner')
df456 = df456[['UnitID', 'Institution Name', '4', '4 Value', '5', '5 Value', '6', '6 Value']]
df456 = df456.loc[:,~df456.columns.duplicated()]
df456['C/B'] = df456['6 Value'] / df456['5 Value']
df456['A-(C/B)'] = df456['4 Value'] - df456['C/B']

deflator = [100.738, 102.515, 104.15, 104.979, 106.487, 108.67, 111.175, 112.978] * 86

df456['deflator'] = df456['A-(C/B)'] / deflator
df456['real market'] = df456['deflator'] * 100


"""df78"""

df7 = pd.read_csv('7. Value of endowment assets at the end of the fiscal year.csv')
df7 = df7[df7.UnitID.isin(empty_id) == False]
df7.dropna(subset = ['Value of endowment assets at the end of the fiscal year (F1112_F2_RV)'], inplace=True)
df7 = (df7.set_index(["UnitID", "Institution Name"])
         .stack()
         .reset_index(name='7 Value')
         .rename(columns={'level_2':'7'}))
