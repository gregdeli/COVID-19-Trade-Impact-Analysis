import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# Load the data
url = "https://www.stats.govt.nz/assets/Uploads/Effects-of-COVID-19-on-trade/Effects-of-COVID-19-on-trade-At-15-December-2021-provisional/Download-data/effects-of-covid-19-on-trade-at-15-december-2021-provisional.csv"
#data = pd.read_csv(url)
data = pd.read_csv("covid-data.csv") #del

# Convert Date to datetime
data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')

# Create the graphs
def create_graph(qdata, groupby_col, title, measure='Both'):
    plt.figure(figsize=(10, 6))
    x_axis = groupby_col
    y_axis = 'Value'
    sns.barplot(x=x_axis, y=y_axis, data=qdata, color='steelblue')  
    plt.title(f"{title} ({measure})")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f"{title} ({measure}).png")
    #plt.show()

# Total turnover per month for each Measure
for measure in data['Measure'].unique():
    monthly_turnover = data[data['Measure'] == measure].groupby(data['Date'].dt.month)['Value'].sum().reset_index()
    create_graph(monthly_turnover, 'Date', 'Monthly Turnover', measure)

# Total turnover per country for each Measure
for measure in data['Measure'].unique():
    country_turnover = data[data['Measure'] == measure].groupby('Country')['Value'].sum().reset_index()
    create_graph(country_turnover,'Country', 'Coutry Turnover', measure)

# Total turnover per transport mode for each Measure
for measure in data['Measure'].unique():
    transport_turnover = data[data['Measure'] == measure].groupby('Transport_Mode')['Value'].sum().reset_index()
    create_graph(transport_turnover, 'Transport_Mode', 'Transport Mode Turnover', measure)

# Total turnover per weekday for each Measure
for measure in data['Measure'].unique():
    weekday_turnover = data[data['Measure'] == measure].groupby('Weekday')['Value'].sum().reset_index()
    create_graph(weekday_turnover, 'Weekday', 'Weekday Turnover', measure)

# Total turnover per commodity category for each Measure
for measure in data['Measure'].unique():
    commodity_turnover = data[data['Measure'] == measure].groupby('Commodity')['Value'].sum().reset_index()
    create_graph(commodity_turnover, 'Commodity', 'Commodity Chategory Turnover', measure)

# Top 5 months with the highest turnover, regardless of transport mode and commodity type
top_months = data.groupby(data['Date'].dt.month)['Value'].sum().nlargest(5).reset_index()
create_graph(top_months, 'Date', 'Top 5 Months with Highest Turnover')

# Top 5 commodity categories with the highest turnover, for each country
for country in data['Country'].unique():
    country_data = data[data['Country'] == country]
    top_commodities = country_data.groupby('Commodity')['Value'].sum().nlargest(5).reset_index()
    create_graph(top_commodities, 'Commodity', f'Top 5 Commodity Categories with Highest Turnover for {country}')

# The date with the highest turnover, for each commodity category
for commodity in data['Commodity'].unique():
    commodity_data = data[data['Commodity'] == commodity]
    top_date = commodity_data.groupby('Date')['Value'].sum().nlargest(1).reset_index()
    create_graph(top_date, 'Date', f'Date with Highest Turnover for {commodity}')

# Load data into MySQL
engine = create_engine('mysql://username:password@localhost/dbname')
data.to_sql('trade_data', con=engine, if_exists='replace')

# Export to .csv
data.to_csv('trade_data.csv', index=False)