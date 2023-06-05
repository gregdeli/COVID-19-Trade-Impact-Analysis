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
def create_graph(df, groupby_col, measure, title):
    df_grouped = df[df['Measure'] == measure].groupby(groupby_col)['Value'].sum().reset_index()
    #gia na einai taksinomimenoi oi mhnes sto erwt. 1
    if groupby_col == 'Month':
        df_grouped = df_grouped.sort_values('Month')
    plt.figure(figsize=(10,6))
    sns.barplot(x=groupby_col, y='Value', data=df_grouped)
    plt.title(f"{title} ({measure})")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f"{title} ({measure}).png")
    #plt.show()


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

