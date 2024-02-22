import pandas as pd


df = pd.read_excel('authorDropdown010.xlsx')
df = df.convert_dtypes()
### Important: Should <NA> values be converted to '' or NULL?
print(df.head(20).to_string())
