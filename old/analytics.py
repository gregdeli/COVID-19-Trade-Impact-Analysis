import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import StringIO

# Download the CSV file
url = "https://www.stats.govt.nz/assets/Uploads/Effects-of-COVID-19-on-trade/Effects-of-COVID-19-on-trade-At-15-December-2021-provisional/Download-data/effects-of-covid-19-on-trade-at-15-december-2021-provisional.csv"
req = requests.get(url)
data = StringIO(req.text)

# Load the data into a pandas DataFrame
df = pd.read_csv(data)

# Create the graphs
def create_graph(df, groupby_col, measure, title, country=None):
    df_grouped = df[df['Measure'] == measure].groupby(groupby_col)['Value'].sum().reset_index()
    #gia na einai taksinomimenoi oi mhnes sto erwt. 1
    if groupby_col == 'Month':
        df_grouped = df_grouped.sort_values('Month')
    plt.figure(figsize=(10,6))
    sns.barplot(x=groupby_col, y='Value', data=df_grouped)
    plt.title(f"{title} ({measure})")
    plt.xticks(rotation=0)
    plt.tight_layout()
    if country:
        plt.savefig(f"{title} ({measure}) - {country}.png")
    else:
        plt.savefig(f"{title} ({measure}).png")
    plt.show()


# Total turnover presentation (value column) per month
df['Month'] = pd.to_datetime(df['Date'], format='%d/%m/%Y').dt.strftime('%b')
df['Month'] =  pd.Categorical(df['Month'], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)

create_graph(df, 'Month', '$', 'Total turnover per month')
create_graph(df, 'Month', 'Tonnes', 'Total turnover per month')

# Total turnover presentation (value column) for each country
create_graph(df, 'Country', '$', 'Total turnover per country')
create_graph(df, 'Country', 'Tonnes', 'Total turnover per country')

# Total turnover presentation (value column) for each means of transport
create_graph(df, 'Transport_Mode', '$', 'Total turnover per transport mode')
create_graph(df, 'Transport_Mode', 'Tonnes', 'Total turnover per transport mode')

# Total turnover presentation (value column) for each day of the week
create_graph(df, 'Weekday', '$', 'Total turnover per weekday')
create_graph(df, 'Weekday', 'Tonnes', 'Total turnover per weekday')

# Total turnover presentation (value column) for each category of goods
create_graph(df, 'Commodity', '$', 'Total turnover per commodity')
create_graph(df, 'Commodity', 'Tonnes', 'Total turnover per commodity')

# Presentation of the 5 months with the highest turnover
def create_top5_graph(df, groupby_col, measure, title):
    df_grouped = df[df['Measure'] == measure].groupby(groupby_col)['Value'].sum().nlargest(5).reset_index()
    if groupby_col == 'Month':
        df_grouped['Month'] = pd.Categorical(df_grouped['Month'], categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], ordered=True)
        df_grouped = df_grouped.sort_values('Month')
    plt.figure(figsize=(10,6))
    sns.barplot(x=groupby_col, y='Value', data=df_grouped)
    plt.title(f"{title} ({measure})")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"{title} ({measure}).png")
    #plt.show()

create_top5_graph(df, 'Month', '$', 'Top 5 months with highest turnover')
create_top5_graph(df, 'Month', 'Tonnes', 'Top 5 months with highest turnover')

# Presentation of the 5 categories of goods with the highest turnover, for each country
df_country_commodity = df.groupby(['Country', 'Commodity', 'Measure'])['Value'].sum().reset_index()
df_country_commodity_top5 = df_country_commodity.groupby(['Country', 'Measure']).apply(lambda x: x.nlargest(5, 'Value')).reset_index(drop=True)
for country in df_country_commodity_top5['Country'].unique():
    df_country = df_country_commodity_top5[df_country_commodity_top5['Country'] == country]
    create_graph(df_country[df_country['Measure'] == '$'], 'Commodity', '$', 'Top 5 commodities with highest turnover', country)
    create_graph(df_country[df_country['Measure'] == 'Tonnes'], 'Commodity', 'Tonnes', 'Top 5 commodities with highest turnover', country)

# Presentation of the day with the highest turnover, for each category of goods
df_commodity_day = df.groupby(['Commodity', 'Weekday', 'Measure'])['Value'].sum().reset_index()
df_commodity_day = df_commodity_day.loc[df_commodity_day.groupby(['Commodity', 'Measure'])['Value'].idxmax()]
create_graph(df_commodity_day[df_commodity_day['Measure'] == '$'], 'Weekday', '$', 'Day with highest turnover per commodity')
create_graph(df_commodity_day[df_commodity_day['Measure'] == 'Tonnes'], 'Weekday', 'Tonnes', 'Day with highest turnover per commodity')