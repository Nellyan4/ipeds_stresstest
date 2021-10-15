import pandas as pd
df = pd.read_csv('University List - 4 Year Private - Not for Profit.csv')
college_id = df['unitid']
list = list(college_id)
print(list)