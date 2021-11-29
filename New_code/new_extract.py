import pandas as pd

"""
df_mix = pd.read_excel('./National_sources/College_Map_Results2021_11_04_13.43.38.xlsx')
df_mix = df_mix.loc[4:]
df_mix['UnitID'] = df_mix['Unnamed: 14'].str[-6:]
unitID_list = list(df_mix['UnitID'])
textfile = open("./National_sources/a_file.txt", "w")
for element in unitID_list:
    textfile.write(element + ",")
textfile.close()
"""

"""Get the empty list of schools"""
df1 = pd.read_csv('./New_sources/1.csv')
df1 = df1.iloc[: , :-1]
empty = df1[df1.isna().any(axis=1)]
empty = empty[['UnitID', 'Institution Name']]

df2 = pd.read_csv('./New_sources/2.csv')
df2 = df2.iloc[: , :-1]
empty2 = df2[df2.isna().any(axis=1)]
empty2 = empty2[['UnitID', 'Institution Name']]

df3 = pd.read_csv('./New_sources/3.csv')
df3 = df3.iloc[: , :-1]
empty3 = df3[df3.isna().any(axis=1)]
empty3 = empty3[['UnitID', 'Institution Name']]

df4 = pd.read_csv('./New_sources/4.csv')
df4 = df4.iloc[: , :-1]
empty4 = df4[df4.isna().any(axis=1)]
empty4 = empty4[['UnitID', 'Institution Name']]

df5 = pd.read_csv('./New_sources/5.csv')
df5 = df5.iloc[: , :-1]
empty5 = df5[df5.isna().any(axis=1)]
empty5 = empty5[['UnitID', 'Institution Name']]

df6 = pd.read_csv('./New_sources/6.csv')
df6 = df6.iloc[: , :-1]
empty6 = df6[df6.isna().any(axis=1)]
empty6 = empty6[['UnitID', 'Institution Name']]

df7 = pd.read_csv('./New_sources/7.csv')
df7.loc[201, 'Value of endowment assets at the end of the fiscal year (F1415_F2_RV)'] = float(789354000)
df7 = df7.iloc[: , :-1]
empty7 = df7[df7.isna().any(axis=1)]
empty7 = empty7[['UnitID', 'Institution Name']]

df8 = pd.read_csv('./New_sources/8.csv')
df8 = df8.iloc[: , :-1]
empty8 = df8[df8.isna().any(axis=1)]
empty8 = empty8[['UnitID', 'Institution Name']]

df9 = pd.read_csv('./New_sources/9.csv')
df9 = df9.iloc[: , :-1]
empty9 = df9[df9.isna().any(axis=1)]
empty9 = empty9[['UnitID', 'Institution Name']]

empty_concat = pd.concat([empty, empty2, empty3, empty4, empty5, empty6, empty7, empty8, empty9]).drop_duplicates()
empty_id = list(empty_concat['UnitID'])
empty_concat.to_csv('./National_sources/college_missing_data.csv')

"""df123"""
# Note that Thomas Jefferson only have 2 years record, so we are omitting it as well.

df1 = pd.read_csv('./New_sources/1.csv')
df1 = df1[df1.UnitID.isin(empty_id) == False]
df1 = df1[df1.columns[::-1]]
df1 = (df1.set_index(["UnitID", "Institution Name"])
       .stack()
       .reset_index(name='First year Value')
       .rename(columns={'level_2': 'First year'}))

df2 = pd.read_csv('./New_sources/2.csv')
df2 = df2[df2.UnitID.isin(empty_id) == False]
df2 = df2[df2.columns[::-1]]
df2 = (df2.set_index(["UnitID", "Institution Name"])
       .stack()
       .reset_index(name='2 Value')
       .rename(columns={'level_2': '2'}))

df3 = pd.read_csv('./New_sources/3.csv')
df3 = df3[df3.UnitID.isin(empty_id) == False]
df3 = df3[df3.columns[::-1]]
df3 = (df3.set_index(["UnitID", "Institution Name"])
       .stack()
       .reset_index(name='3 Value')
       .rename(columns={'level_2': '3'}))

df23 = pd.concat([df2, df3], axis=1, join='inner')
df23 = df23[['UnitID', 'Institution Name', '2', '2 Value', '3', '3 Value']]
df23['Retention'] = df23['3 Value'] / df23['2 Value']

df123 = pd.concat([df1, df23], axis=1, join='inner')
df123 = df123[
    ['UnitID', 'Institution Name', 'First year', 'First year Value', '2', '2 Value', '3', '3 Value', 'Retention']]

df123 = df123.loc[:, ~df123.columns.duplicated()]

"""df456"""

df4 = pd.read_csv('./New_sources/4.csv')
df4 = df4[df4.UnitID.isin(empty_id) == False]
df4 = df4[df4.columns[::-1]]
df4 = (df4.set_index(["UnitID", "Institution Name"])
       .stack()
       .reset_index(name='4 Value')
       .rename(columns={'level_2': '4'}))

df5 = pd.read_csv('./New_sources/5.csv')
df5 = df5[df5.UnitID.isin(empty_id) == False]
df5 = df5[df5.columns[::-1]]
df5 = (df5.set_index(["UnitID", "Institution Name"])
       .stack()
       .reset_index(name='5 Value')
       .rename(columns={'level_2': '5'}))

df6 = pd.read_csv('./New_sources/6.csv')
df6 = df6[df6.UnitID.isin(empty_id) == False]
df6 = df6[df6.columns[::-1]]
df6 = (df6.set_index(["UnitID", "Institution Name"])
       .stack()
       .reset_index(name='6 Value')
       .rename(columns={'level_2': '6'}))

df456 = pd.concat([df4, df5, df6], axis=1, join='inner')
df456 = df456[['UnitID', 'Institution Name', '4', '4 Value', '5', '5 Value', '6', '6 Value']]
df456 = df456.loc[:, ~df456.columns.duplicated()]
df456['C/B'] = df456['6 Value'] / df456['5 Value']
df456['A-(C/B)'] = df456['4 Value'] - df456['C/B']

deflator = [100.738, 102.515, 104.15, 104.979, 106.487, 108.67, 111.175, 112.978] * 968

df456['deflator'] = df456['A-(C/B)'] / deflator
df456['real market'] = df456['deflator'] * 100

"""df78"""

df7 = pd.read_csv('./New_sources/7.csv')
df7.loc[201, 'Value of endowment assets at the end of the fiscal year (F1415_F2_RV)'] = float(789354000)
df7 = df7[df7.UnitID.isin(empty_id) == False]
df7 = df7[df7.columns[::-1]]
df7 = (df7.set_index(["UnitID", "Institution Name"])
       .stack()
       .reset_index(name='7 Value')
       .rename(columns={'level_2': '7'}))

df8 = pd.read_csv('./New_sources/8.csv')
df8 = df8[df8.UnitID.isin(empty_id) == False]
df8 = df8[df8.columns[::-1]]
df8 = (df8.set_index(["UnitID", "Institution Name"])
       .stack()
       .reset_index(name='8 Value')
       .rename(columns={'level_2': '8'}))

df9 = pd.read_csv('./New_sources/9.csv')
df9 = df9[df9.UnitID.isin(empty_id) == False]
df9 = df9.iloc[: , :-1]
df9 = df9.fillna(0)
df9 = df9[df9.columns[::-1]]
df9 = (df9.set_index(["UnitID", "Institution Name"])
       .stack()
       .reset_index(name='9 Value')
       .rename(columns={'level_2': '9'}))


df78 = pd.concat([df7, df8, df9], axis=1, join='inner')
df78 = df78[['UnitID', 'Institution Name', '7', '7 Value', '8', '8 Value', '9', '9 Value']]

df78['Endowment/expenses'] = df78['7 Value'] / (df78['8 Value'] - df78['9 Value'])

"""Merge all"""

df_all = pd.concat([df123, df456, df78], axis=1, join='inner')
df_all = df_all.loc[:, ~df_all.columns.duplicated()]
df_ready = df_all[['UnitID', 'Institution Name', 'First year Value', 'Retention', 'real market', 'Endowment/expenses']]
year_list = ['2012 (Base)', '2013', '2014', '2015', '2016', '2017', '2018', '2019'] * 968
count = [1, 2, 3, 4, 5, 6, 7, 8] * 968
df_ready.insert(1, 'Counter', count)
df_ready.insert(2, 'Year', year_list)

#df_ready.sort_values(by=['UnitID'], ascending=False).sort_values(by=['Counter'], ascending=False)
#df_ready.groupby('UnitID', sort=False).apply(lambda x: x.iloc[::-1]).reset_index(drop=True)

writer = pd.ExcelWriter('./New_sources/cleaned_data.xlsx')
# write dataframe to excel
df_ready.to_excel(writer)
# save the excel
writer.save()
writer.close()

writer = pd.ExcelWriter('./New_sources/cleaned_data_raw.xlsx')
df_all.to_excel(writer)
writer.save()
writer.close()

"""Calculate the threshold"""


#123 test test