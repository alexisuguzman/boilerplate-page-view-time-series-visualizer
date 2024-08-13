import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.) 
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True) 

# Clean data 
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))] 

def draw_line_plot(): 
    # Draw line plot 
    df_line = df.copy().reset_index()  

    fig, ax = plt.subplots(figsize=(15,5))
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.ylabel("Page Views")
    plt.xlabel("Date") 

    sns.lineplot(data=df_line, x='date', y='value') 

    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    # Step 1: Create a copy of the DataFrame and reset the index
    df_bar = df.copy()
    df_bar.reset_index(inplace=True)

    # Step 2: Ensure 'date' is a datetime object
    df_bar['date'] = pd.to_datetime(df_bar['date'])

    # Step 3: Extract the year and month as separate columns
    df_bar['year'] = df_bar['date'].dt.year
    df_bar['month'] = df_bar['date'].dt.strftime('%B')  # Converts month number to month name

    # Step 4: Group by year and month, then calculate the average of 'value'
    df_grouped = df_bar.groupby(['year', 'month'], as_index=False)['value'].mean()

    # Define the correct order for the months
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # Step 5: Sort the DataFrame by year and month for correct plotting order
    df_grouped['month'] = pd.Categorical(df_grouped['month'], categories=month_order, ordered=True)
    df_grouped.sort_values(by=['year', 'month'], inplace=True)

    fig, ax = plt.subplots(figsize=(10, 10))
    sns.barplot(data=df_grouped, x='year', y='value', hue='month', ax=ax)

    plt.title("Average Page Views per Month by Year")
    plt.ylabel("Average Page Views")
    plt.xlabel("Years")
    plt.legend(title='Month')
    print(len([rect for rect in ax.get_children() if isinstance(rect, mpl.patches.Rectangle)]))

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box['date']]

    # Define the correct order for the months
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Convert the 'month' column to a categorical type with the correct order
    df_box['month'] = pd.Categorical(df_box['month'], categories=month_order, ordered=True)

    
    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(25,10))

    sns.boxplot(x='year', y='value', data=df_box, ax=ax[0], hue='year')

    ax[0].set_title("Year-wise Box Plot (Trend)")
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel("Page Views")

    sns.boxplot(x='month', y='value', data=df_box, ax=ax[1], hue='month')

    ax[1].set_title("Month-wise Box Plot (Seasonality)")
    ax[1].set_xlabel("Month")
    ax[1].set_ylabel("Page Views")


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

draw_bar_plot()