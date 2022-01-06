import pandas as pd



df = pd.read_csv(
	'data/2020-2021_SHSAT_Admissions_Test_Offers_By_Sending_School.csv'
	)

print(df.head())

print(df['Number of Offers'].unique())