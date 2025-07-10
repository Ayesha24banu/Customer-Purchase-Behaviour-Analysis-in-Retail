import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import os 

#plot setting
sns.set(style= 'whitegrid')

# --- Exploratory Data Analysis (EDA) ---

#1. Top-Selling Products(10)
# Groups data by product description, sums quantities, and displays top 10 products
def top_selling_products(df: pd.DataFrame):
    top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
    print("\nTop 10 Selling Products:")
    print(top_products)

    #plot the graphs 
    plt.figure(figsize=(10,6))
    top_products.sort_values().plot(kind = 'barh', color= 'skyblue')
    plt.title('Top 10 best-selling products', fontsize=14, fontweight='bold')
    plt.xlabel('Total Quantity sold')
    plt.ylabel('Product')
    plt.tight_layout()
    plt.savefig(r'../outputs/figures/eda_fig/top_products.png')
    plt.show()
    plt.close()

# 2. Revenue Trends
# 2a. Monthly Revenue Trend
# Aggregates revenue by month and plots trend
def monthly_revenue_trend(df: pd.DataFrame):
    # Add 'Month' for trend analysis
   df['Month']= df['InvoiceDate'].dt.to_period('M')

   monthly_revenue = df.groupby('Month')['TotalPrice'].sum()
   print("\nMonthly Revenue:")
   print(monthly_revenue)

   # Stats
   high_month = monthly_revenue.idxmax()
   low_month = monthly_revenue.idxmin()
   avg_revenue = monthly_revenue.mean()

   #plot the graphs
   plt.figure(figsize=(14,6))
   monthly_revenue.plot(kind='line',marker = 'o')

   # Plot green/red segments
   months = monthly_revenue.index.tolist()
   values = monthly_revenue.values

   for i in range(len(values) - 1):
       x = [months[i], months[i+1]]
       y = [values[i], values[i+1]]
       color = 'green' if values[i+1] > values[i] else 'red'
       plt.plot(x, y, color=color, linewidth=2)

   # Add points + highlights
   plt.plot(months, values, marker='o', color='black', linewidth=1, label='Monthly Points')
   # Highlight high
   plt.plot(high_month, monthly_revenue[high_month], 'go', label=' Highest', markersize=15)
   # Highlight low
   plt.plot(low_month, monthly_revenue[low_month], 'ro', label=' Lowest', markersize=15)
   # Highlight average line
   plt.axhline(avg_revenue, color='blue', linestyle='--', linewidth=1.5, label=f'Avg Revenue (£{int(avg_revenue):,})')

   # Add data labels to each month
   for x, y in monthly_revenue.items():
       plt.text(x, y + 10000, f"£{int(y):,}", ha='center', va='bottom', fontsize=9, rotation=0)

   # Design the layout
   plt.title('Monthly Revenue Trend', fontsize=14, fontweight='bold')
   plt.xlabel('Months')
   plt.ylabel('Revenue (£)')
   plt.xticks(rotation=45)
   plt.grid(True)
   plt.legend()
   plt.tight_layout()
   plt.savefig(r'../outputs/figures/eda_fig/Monthly Revenue Trend.png')
   plt.show()
   plt.close()

# 2b. Daily Revenue Trend
# Tracks day-wise sales and plots smoothed trend
def daily_revenue_trend(df: pd.DataFrame):
    # Add 'Daily' for trend analysis
    df['Daily']= df['InvoiceDate'].dt.date
    daily_revenue = df.groupby('Daily')['TotalPrice'].sum()
    print("\nDaily Revenue:")
    print(daily_revenue)

    # Stats
    high_day = daily_revenue.idxmax()
    low_day = daily_revenue.idxmin()
    avg_day_rev = daily_revenue.mean()

    #plot the graphs
    plt.figure(figsize=(14,6))
    daily_revenue.plot(color='brown', alpha=0.5, label='Daily')
    daily_revenue.rolling(7).mean().plot(color='blue', label='7-Day Avg')

    # Highlight points
    plt.plot(high_day, daily_revenue[high_day], 'go', label='Highest', markersize=8)
    plt.plot(low_day, daily_revenue[low_day], 'ro', label='Lowest', markersize=8)
    plt.axhline(avg_day_rev, color='black', linestyle='--', linewidth=1, label=f'Avg Daily (£{int(avg_day_rev):,})')

    # Design the layout
    plt.title('Daily Revenue Trend', fontsize=14, fontweight='bold')
    plt.xlabel('Daily')
    plt.ylabel('Revenue')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(r'../outputs/figures/eda_fig/Daily Revenue Trend.png')
    plt.show()
    plt.close()

#3. Purchase Time Analysis (Peak Hours)
# Analyzes purchase volume by hour of day
def hourly_revenue_trend(df: pd.DataFrame):
    # Add 'Hours' for Time analysis
    df['Hour'] = df['InvoiceDate'].dt.hour
    hourly_sales = df.groupby('Hour')['TotalPrice'].sum().sort_index()
    print("\nHourly sales:")
    print(hourly_sales)

    #plot the graphs
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x=hourly_sales.index, y=hourly_sales.values, palette="viridis")

    # Add data labels on top of bars
    for i, value in enumerate(hourly_sales.values):
        ax.text(i, value + 1000, f"£{int(value):,}", ha='center', fontsize=8)

    # Design the layout
    plt.title(" Revenue by Hour of Day", fontsize=14, fontweight='bold')
    plt.xlabel("Hour (24-hour format)")
    plt.ylabel("Total Revenue")
    plt.tight_layout()
    plt.grid(True)
    plt.savefig('../outputs/figures/eda_fig/revenue_by_hour.png')
    plt.show()
    plt.close()

#4. Revenue by Country
# Identifies top 10 countries by total revenue
def revenue_by_country(df: pd.DataFrame):
    country_revenue = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(10)
    print("\nTop 10 Countries by Revenue:")
    print(country_revenue)

    #plot the graphs
    plt.figure(figsize=(12, 6))
    country_revenue.plot(kind='bar', color='coral')

    #Add value labels on top
    for i, v in enumerate(country_revenue.values):
        plt.text(i, v + 10000, f"£{int(v):,}", ha='center', fontsize=9)

    # Design the layout
    plt.title('Top 10 Countries by Revenue', fontsize=14, fontweight='bold')
    plt.xlabel('Country')
    plt.ylabel('Total Revenue')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('../outputs/figures/eda_fig/revenue_by_country.png')
    plt.show()
    plt.close()

# Combined EDA run function
def run_eda(df: pd.DataFrame):
    top_selling_products(df)
    monthly_revenue_trend(df)
    daily_revenue_trend(df)
    hourly_revenue_trend(df)
    revenue_by_country(df)