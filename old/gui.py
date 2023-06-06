
def menu():
    # GUI Menu 

    # Create a new Tkinter window
    window = tk.Tk()
    window.title("Graph Selector")

    # Create buttons
    button1 = tk.Button(window, text="Days with the highest Turnovers", command=lambda: covid19_tables.top_date_per_commodity())
    button2 = tk.Button(window, text="Top 5 Commodities for each Country", command=lambda: covid19_tables.top5_commodities_per_country())
    button3 = tk.Button(window, text="Top 5 Months with the biggest Turnover", command=lambda: covid19_tables.top5_months())
    button3 = tk.Button(window, text="Total turnover per commodity category ($)", command=lambda: covid19_tables.commodity_turnover())
    button3 = tk.Button(window, text="Top 5 Months with the biggest Turnover", command=lambda: show_image("Top 5 Months with the biggest Turnover"))
    button3 = tk.Button(window, text="Top 5 Months with the biggest Turnover", command=lambda: show_image("Top 5 Months with the biggest Turnover"))
    button3 = tk.Button(window, text="Top 5 Months with the biggest Turnover", command=lambda: show_image("Top 5 Months with the biggest Turnover"))
    button3 = tk.Button(window, text="Top 5 Months with the biggest Turnover", command=lambda: show_image("Top 5 Months with the biggest Turnover"))
    button3 = tk.Button(window, text="Top 5 Months with the biggest Turnover", command=lambda: show_image("Top 5 Months with the biggest Turnover"))
    button3 = tk.Button(window, text="Top 5 Months with the biggest Turnover", command=lambda: show_image("Top 5 Months with the biggest Turnover"))
    button3 = tk.Button(window, text="Top 5 Months with the biggest Turnover", command=lambda: show_image("Top 5 Months with the biggest Turnover"))
    button3 = tk.Button(window, text="Top 5 Months with the biggest Turnover", command=lambda: show_image("Top 5 Months with the biggest Turnover"))
    # And so on for all your graphs...

    # Pack the buttons so they are visible
    button1.pack()
    button2.pack()
    button3.pack()
    button3.pack()
    button3.pack()
    button3.pack()
    button3.pack()
    button3.pack()
    button3.pack()
    button3.pack()
    button3.pack()
    button3.pack()
    # And so on for all your buttons...

    # Start the event loop
    window.mainloop()


