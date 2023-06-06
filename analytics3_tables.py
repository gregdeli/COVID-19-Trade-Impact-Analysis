import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sqlalchemy import create_engine

# Load the data
url = "https://www.stats.govt.nz/assets/Uploads/Effects-of-COVID-19-on-trade/Effects-of-COVID-19-on-trade-At-15-December-2021-provisional/Download-data/effects-of-covid-19-on-trade-at-15-december-2021-provisional.csv"
#data = pd.read_csv(url) # import data into a pandas data frame
data = pd.read_csv("covid-data.csv") #del

# Create a connection to your MySQL server
engine = create_engine('mysql+pymysql://root:giagia12@localhost:3306/covid_19_data')

# Dhmiourgia fakelou me tis eikones grafimatwn
os.makedirs('graphs', exist_ok=True)
# Dhmiourgia fakelou me ta csv
os.makedirs('csv_files', exist_ok=True)

# Create the graphs
def create_graph(qdata, title, x_axis, y_axis, hue=None):
    # Create a figure and a set of subplots
    fig, ax = plt.subplots(figsize=(10, 6))
    hue = hue
    # Create a bar plot
    sns.barplot(data=qdata, x=x_axis, y=y_axis, hue=hue, ax=ax)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(f"graphs/{title}.png")

# Convert Date to datetime
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')

# Total turnover per month for each Measure
for measure in data['Measure'].unique():
    monthly_turnover = data[data['Measure'] == measure].groupby(data['Date'].dt.month)['Value'].sum().reset_index()
    create_graph(monthly_turnover, f"Total Turnover per Month ({measure})", 'Date', 'Value')
    # Prosthiki stin vasi
    monthly_turnover.to_sql(name=f"monthly_turnover_{measure.lower()}", con=engine, if_exists='replace', index=False)
    monthly_turnover.to_csv(f"csv_files/monthly_turnover_{measure.lower()}.csv", index=False)

# Total turnover per country for each Measure
for measure in data['Measure'].unique():
    country_turnover = data[data['Measure'] == measure].groupby('Country')['Value'].sum().reset_index()
    create_graph(country_turnover, f"Total Turnover per Country ({measure})", 'Country', 'Value')
    country_turnover.to_sql(name=f"turnover_per_country_{measure.lower()}", con=engine, if_exists='replace', index=False)
    country_turnover.to_csv(f"csv_files/turnover_per_country_{measure.lower()}.csv", index=False)

# Total turnover per transport mode for each Measure
for measure in data['Measure'].unique():
    transport_turnover = data[data['Measure'] == measure].groupby('Transport_Mode')['Value'].sum().reset_index()
    create_graph(transport_turnover,f"Total Turnover per Transport Mode ({measure})", 'Transport_Mode', 'Value')
    transport_turnover.to_sql(name=f"turnover_per_transport_mode_{measure.lower()}", con=engine, if_exists='replace', index=False)
    transport_turnover.to_csv(f"csv_files/turnover_per_transport_mode_{measure.lower()}.csv", index=False)

# Total turnover per weekday for each Measure
for measure in data['Measure'].unique():
    weekday_turnover = data[data['Measure'] == measure].groupby('Weekday')['Value'].sum().reset_index()
    weekday_turnover.to_sql(name=f"turnover_per_week_{measure.lower()}", con=engine, if_exists='replace', index=False)
    weekday_turnover.to_csv(f"csv_files/turnover_per_week_{measure.lower()}.csv", index=False)

# Total turnover per commodity category for each Measure
for measure in data['Measure'].unique():
    commodity_turnover = data[data['Measure'] == measure].groupby('Commodity')['Value'].sum().reset_index()
    create_graph(commodity_turnover, f"Total turnover per commodity category ({measure})", 'Commodity', 'Value')
    commodity_turnover.to_sql(name=f"turnover_per_commodity_{measure.lower()}", con=engine, if_exists='replace', index=False)
    commodity_turnover.to_csv(f"csv_files/turnover_per_commodity_{measure.lower()}.csv", index=False)

# Top 5 Months with the biggest Turnover
top5_months = data.groupby(data['Date'].dt.month)['Value'].sum().nlargest(5).reset_index()
create_graph(top5_months, 'Top 5 Months with the biggest Turnover', 'Date', 'Value')
top5_months.to_sql(name=f"top5_months", con=engine, if_exists='replace', index=False)
top5_months.to_csv(f"csv_files/top5_months.csv", index=False)

# Top 5 Commodities with the biggest Turnover for each Country 
commodity_country_turnover = data.groupby(['Commodity', 'Country'])['Value'].sum().reset_index()
# Sort by 'Country' and 'Value', then group by 'Country' and take the top 5 commodities for each country
top5_commodities_per_country = commodity_country_turnover.sort_values(['Country', 'Value'], ascending=[True, False]).groupby('Country').head(5)
create_graph(top5_commodities_per_country, 'Top 5 Commodities for each Country', 'Country', 'Value', 'Commodity')
top5_commodities_per_country.to_sql(name=f"top5_commodities_per_country", con=engine, if_exists='replace', index=False)
top5_commodities_per_country.to_csv(f"csv_files/top5_commodities_per_country.csv", index=False)

# Calculate total turnover for each date for each commodity
date_commodity_turnover = data.groupby(['Date', 'Commodity'])['Value'].sum().reset_index()
# Sort by 'Commodity' and 'Value', then group by 'Commodity' and take the date with the highest turnover for each commodity
top_date_per_commodity = date_commodity_turnover.sort_values(['Commodity', 'Value'], ascending=[True, False]).groupby('Commodity').head(1)
create_graph(top_date_per_commodity, 'Days with the highest Turnovers', 'Date', 'Value', 'Commodity')
top_date_per_commodity.to_sql(name=f"top_date_per_commodity", con=engine, if_exists='replace', index=False)
top_date_per_commodity.to_csv(f"csv_files/top_date_per_commodity.csv", index=False)
