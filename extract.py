import pandas as pd

"""Get the list of university ID"""
df = pd.read_csv('University List - 4 Year Private - Not for Profit.csv')
college_id = df['unitid']
list = list(college_id)

"""Get the empty list of schools"""
df2 = pd.read_csv('1. Grand total (EF2019  All students  Undergraduate  Degree:certificate-seeking  First-time).csv')
empty = df2[df2['Grand total (EF2019  All students  Undergraduate  Degree/certificate-seeking  First-time)'].isna()]
empty = empty[['UnitID', 'Institution Name']]

empty.to_csv('college_missing_data.csv')