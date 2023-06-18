import sys
import pandas as pd

month = sys.argv[1]
year = sys.argv[2]

all_assets = pd.read_csv(f"../datasources/{year}/{month}/monthly_asset.csv", parse_dates=["Date"])
apptech = all_assets[all_assets['Symbol'] == 'APCX']
apptech['Intraday_Delta'] = apptech['Adj Close'] - apptech['Open']

kept_values = ['Open', 'Adj Close', 'Intraday_Delta']
apptech[kept_values].to_csv(f'../datasources/{year}/{month}/report_AppTech.csv', index = False)



