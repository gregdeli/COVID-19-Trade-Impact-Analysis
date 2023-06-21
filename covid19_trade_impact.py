import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os
import tkinter as tk

def load_data(username, password, dbase_name):
    # Load the data
    url = "https://www.stats.govt.nz/assets/Uploads/Effects-of-COVID-19-on-trade/Effects-of-COVID-19-on-trade-At-15-December-2021-provisional/Download-data/effects-of-covid-19-on-trade-at-15-december-2021-provisional.csv"
    global data
    data = pd.read_csv(url) # import data into a pandas data frame
    # Convert Date to datetime
    data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%Y')

    # Create a connection to your MySQL server
    global engine
    engine = create_engine(f"mysql+pymysql://{username}:{password}@localhost:3306/{dbase_name}")

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
    plt.show()


# Kathe mia apo tis parakatw synartiseis ftiaxnei enan apo tous zitoumenous pinakes,
# ton opoio kanei plot, apothikeuei stin mysql vasi kai kanei export ws csv 

def monthly_turnover(measure):
    # Total turnover per month for each Measure
    monthly_turnover = data[data['Measure'] == measure].groupby(data['Date'].dt.month)['Value'].sum().reset_index()
    # Prosthiki stin vasi
    monthly_turnover.to_sql(name=f"monthly_turnover_{measure.lower()}", con=engine, if_exists='replace', index=False)
    monthly_turnover.to_csv(f"csv_files/monthly_turnover_{measure.lower()}.csv", index=False)
    create_graph(monthly_turnover, f"Total Turnover per Month ({measure})", 'Date', 'Value')
    
def country_turnover(measure):
    # Total turnover per country each Measure
    country_turnover = data[data['Measure'] == measure].groupby('Country')['Value'].sum().reset_index()
    country_turnover.to_sql(name=f"turnover_per_country_{measure.lower()}", con=engine, if_exists='replace', index=False)
    country_turnover.to_csv(f"csv_files/turnover_per_country_{measure.lower()}.csv", index=False)
    create_graph(country_turnover, f"Total Turnover per Country ({measure})", 'Country', 'Value')
    
def transport_turnover(measure):
    # Total turnover per transport mode for each Measure
    transport_turnover = data[data['Measure'] == measure].groupby('Transport_Mode')['Value'].sum().reset_index()
    transport_turnover.to_sql(name=f"turnover_per_transport_mode_{measure.lower()}", con=engine, if_exists='replace', index=False)
    transport_turnover.to_csv(f"csv_files/turnover_per_transport_mode_{measure.lower()}.csv", index=False)
    create_graph(transport_turnover,f"Total Turnover per Transport Mode ({measure})", 'Transport_Mode', 'Value')
    
def weekday_turnover(measure):
    # Total turnover per weekday for each Measure
    weekday_turnover = data[data['Measure'] == measure].groupby('Weekday')['Value'].sum().reset_index()
    weekday_turnover.to_sql(name=f"turnover_per_week_{measure.lower()}", con=engine, if_exists='replace', index=False)
    weekday_turnover.to_csv(f"csv_files/turnover_per_week_{measure.lower()}.csv", index=False)
    create_graph(weekday_turnover, f"Total turnover per Weekday ({measure})", 'Weekday', 'Value')

def commodity_turnover(measure):
    # Total turnover per commodity category for each Measure
    commodity_turnover = data[data['Measure'] == measure].groupby('Commodity')['Value'].sum().reset_index()
    commodity_turnover.to_sql(name=f"turnover_per_commodity_{measure.lower()}", con=engine, if_exists='replace', index=False)
    commodity_turnover.to_csv(f"csv_files/turnover_per_commodity_{measure.lower()}.csv", index=False)
    create_graph(commodity_turnover, f"Total turnover per commodity category ({measure})", 'Commodity', 'Value')

def top5_months():
    # Top 5 Months with the biggest Turnover
    top5_months = data.groupby(data['Date'].dt.month)['Value'].sum().nlargest(5).reset_index()
    top5_months.to_sql(name=f"top5_months", con=engine, if_exists='replace', index=False)
    top5_months.to_csv(f"csv_files/top5_months.csv", index=False)
    create_graph(top5_months, 'Top 5 Months with the biggest Turnover', 'Date', 'Value')
    
def top5_commodities_per_country():
    # Top 5 Commodities with the biggest Turnover for each Country 
    commodity_country_turnover = data.groupby(['Commodity', 'Country'])['Value'].sum().reset_index()
    # Sort by 'Country' and 'Value', then group by 'Country' and take the top 5 commodities for each country
    top5_commodities_per_country = commodity_country_turnover.sort_values(['Country', 'Value'], ascending=[True, False]).groupby('Country').head(5)
    top5_commodities_per_country.to_sql(name=f"top5_commodities_per_country", con=engine, if_exists='replace', index=False)
    top5_commodities_per_country.to_csv(f"csv_files/top5_commodities_per_country.csv", index=False)
    create_graph(top5_commodities_per_country, 'Top 5 Commodities for each Country', 'Country', 'Value', 'Commodity')

def top_date_per_commodity():
    # Calculate total turnover for each date for each commodity
    date_commodity_turnover = data.groupby(['Date', 'Commodity'])['Value'].sum().reset_index()
    # Sort by 'Commodity' and 'Value', then group by 'Commodity' and take the date with the highest turnover for each commodity
    top_date_per_commodity = date_commodity_turnover.sort_values(['Commodity', 'Value'], ascending=[True, False]).groupby('Commodity').head(1)
    top_date_per_commodity.to_sql(name=f"top_date_per_commodity", con=engine, if_exists='replace', index=False)
    top_date_per_commodity.to_csv(f"csv_files/top_date_per_commodity.csv", index=False)
    create_graph(top_date_per_commodity, 'Days with the highest Turnovers', 'Date', 'Value', 'Commodity')

#main:

# Dhmiourgia fakelou me tis eikones grafimatwn
os.makedirs('graphs', exist_ok=True)
# Dhmiourgia fakelou me ta csv
os.makedirs('csv_files', exist_ok=True)

load_data('root', '12345678', 'dbase-name')

# GUI Menu 

# Create a new Tkinter window
window = tk.Tk()
window.title("Graph Selector")

# Create buttons
button1 = tk.Button(window, text="Days with the highest Turnovers", command=lambda: top_date_per_commodity())
button2 = tk.Button(window, text="Top 5 Commodities for each Country", command=lambda: top5_commodities_per_country())
button3 = tk.Button(window, text="Top 5 Months with the biggest Turnover", command=lambda: top5_months())
button4 = tk.Button(window, text="Total turnover per commodity category ($)", command=lambda: commodity_turnover('$'))
button5 = tk.Button(window, text="Total turnover per commodity category (Tonnes)", command=lambda: commodity_turnover('Tonnes'))
button6 = tk.Button(window, text="Total Turnover per Weekday ($)", command=lambda: weekday_turnover('$'))
button7 = tk.Button(window, text="Total Turnover per Weekday (Tonnes)", command=lambda: weekday_turnover('Tonnes'))
button8 = tk.Button(window, text="Total Turnover per Country ($)", command=lambda: country_turnover('$'))
button9 = tk.Button(window, text="Total Turnover per Country (Tonnes)", command=lambda: country_turnover('Tonnes'))
button10 = tk.Button(window, text="Total Turnover per Month ($)", command=lambda: monthly_turnover('$'))
button11 = tk.Button(window, text="Total Turnover per Month (Tonnes)", command=lambda: monthly_turnover('Tonnes'))
button12 = tk.Button(window, text="Total Turnover per Transport Mode ($)", command=lambda: transport_turnover('$'))
button13 = tk.Button(window, text="Total Turnover per Transport Mode (Tonnes)", command=lambda: transport_turnover('Tonnes'))

# Pack the buttons so they are visible
button1.pack()
button2.pack()
button3.pack()
button4.pack()
button5.pack()
button6.pack()
button7.pack()
button8.pack()
button9.pack()
button10.pack()
button11.pack()
button12.pack()
button13.pack()

# Start the event loop
window.mainloop()