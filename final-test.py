import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates

st.title('Sports Betting in Connecticut')
st.header('by: Matt Rice')
st.subheader('DTS 205 Final Project')        

url = 'https://raw.githubusercontent.com/Rice-Matt/final_project/main/Selected_Online_Sport_Wagering_Data_20240806.csv' 

df = pd.read_csv(url)

st.write('Here is the data I am looking at for this project:')
st.dataframe(df, width = 800, height = 300)

st.text('There are three legal sports betting licensees in Connecticut')
st.markdown(
"""
Licensees:
- CT Lottery Corp
- Mohegan Digital
- MPI Master Wagering
"""
)

st.header('How Profitable are these Licensee?')

df['Month Ending'] = pd.to_datetime(df['Month Ending'], format='%m/%d/%Y %I:%M:%S %p')

licensees = df['Licensee'].unique()
fig, ax = plt.subplots(figsize=(12, 6))  

for licensee in licensees:
    licensee_data = df[df['Licensee'] == licensee]
    monthly_profits = licensee_data.groupby('Month Ending')['Total Gross Gaming Revenue'].sum()
    ax.plot(monthly_profits.index, monthly_profits.values / 1e6, label=licensee)

ax.set_xlabel('Month Ending')
ax.set_ylabel('Total Gross Gaming Revenue (Millions)')
ax.set_title('Total Licensee Monthly Profits')
plt.xticks(rotation=45)
ax.legend()
fig.tight_layout()

def millions(x, pos):
    return '{:.0f}M'.format(x)

formatter = FuncFormatter(millions)
ax.yaxis.set_major_formatter(formatter)

st.pyplot(fig)

st.text('None of the Licensees have ever had a month where they did not make a profit')

st.subheader('\nHighest Indivdual Monthly Profits')
genre = st.radio(
    "Select a Licensee",
    ('CT Lottery', 'Mohegan Digital', 'MPI Master Wagering'))
if genre == 'CT Lottery':
    st.write('$1,109,979 total gross profit for October in 2023')
if genre == 'Mohegan Digital':
    st.write('10,968,556 total gross profit for January 2024')
if genre == 'MPI Master Wagering':
    st.write("$8,045,409 total gross profit for January 2024")

st.header('How much tax revenue is CT making from sports betting?')

yearly_taxes = df.groupby(df['Month Ending'].dt.year)['Federal Excise Tax (4)'].sum()
yearly_taxes.index = pd.to_datetime(yearly_taxes.index, format='%Y')


fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot(111)
ax.bar(yearly_taxes.index, yearly_taxes.values, width=100)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y')) 
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.set_xlabel('Year')
ax.set_ylabel('Total Taxes Paid')
ax.set_title('Combined Total Taxes Paid Yearly by Licensees')
def millions_formatter(x, pos):
    return f'{x / 1e6:.1f}M'

ax.yaxis.set_major_formatter(FuncFormatter(millions_formatter))
plt.xticks(rotation=45)
fig.tight_layout()


col1, col2 = st.columns(2)
with col1:
    st. pyplot(fig)
with col2:
    yearly_taxes = df.groupby(df['Month Ending'].dt.year)['Federal Excise Tax (4)'].sum()
    selected_year = st.selectbox('Select Year', yearly_taxes.index)
    st.write(f"Total taxes paid in {selected_year}: ${yearly_taxes[selected_year]:,.2f}")


st.markdown(
"""
For 2023 where the state collect $4,005,449 from these Licensees, let's look at Southerns state funding
"""
)

from PIL import Image
southern_tax = Image.open('S-Tax.jpg')
st.image(southern_tax, use_column_width=True)

st.header('How big of a problem is sports betting?')
st.write('For this I wanted to see how much Money CT residents spent on sports betting')

yearly_win_loss = df.groupby(df['Month Ending'].dt.year)['Online Sports Wagering Win/(Loss)'].sum()
selected_year = st.selectbox('Select Year', yearly_win_loss.index, key='win_loss_year')
st.write(f"Total spent on sports betting {selected_year}: ${yearly_win_loss[selected_year]:,.2f}")

st.subheader('how does that compare to other "vices"')
st.write('to compare to other things, I looked at another data set with all Connect tax revenue information')

URL2= "https://raw.githubusercontent.com/Rice-Matt/final_project/main/Tax_Revenue_by_Month_20240807.csv"
df2= pd.read_csv(URL2)

st.dataframe(df2, width = 800, height = 300)

df_2023 = df2[df2['Calendar Year'] == 2023]

total_alcoholic_tax_2023 = df_2023['Alcoholic Beverages'].sum()
total_tobacco_tax_2023 = df_2023['Tobacco Products'].sum()
total_cannabis_tax_2023 = df_2023['Cannabis Tax'].sum()


st.write('In 2023:')
st.write('-Total Alcholic Beverages Tax $79,839,831')
st.write('-Total Tobacco Products Tax $16,049,606')
st.write('-Total Cannabis Tax $13,709,333')
st.write('-Total Licensee Tax $4,005,449')


labels = ['Alcoholic Beverages', 'Tobacco Products', 'Cannabis Tax', 'Licensee Tax']
sizes = [total_alcoholic_tax_2023, total_tobacco_tax_2023, total_cannabis_tax_2023, 4005449.00]

explode = (0, 0, 0, 0.1) 

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%', explode=explode)
ax.axis('equal')  

st.subheader('Total Tax Revenue from CT in 2023')
st.pyplot(fig)

st.header('Betting randomizer from the Mach 2024 data')

import random

metrics = {
    "CT Lottery in March 2024": 0.39, 
    "Mohegan Digital in March 2024": 0.41, 
    "MPI Master Wagering in March 2024": 0.47  
}
def calculate_outcome(bet, metric):
  potential_win = bet * (1 + metric) 
  potential_loss = bet * (1 - metric)
  return potential_win, potential_loss

selected_metric_name = st.selectbox("Select a metric:", list(metrics.keys()))
selected_metric = metrics[selected_metric_name]

bet_amount = st.number_input("Enter your bet amount: ", min_value=0.0, value=10.0, step=0.01)

potential_win, potential_loss = calculate_outcome(bet_amount, selected_metric)
if random.random() < 0.35:  
    st.write(f"You Won!: ${potential_win:.2f}")
else:
    st.write(f"you Lost: ${potential_loss:.2f}")


st.header('What I have learned from looking at this data')
st.markdown(
"""
I am sure to no one's surpise, these Licensees make a lot of money and gambling is not something
that is profitable. I was surprised at how much they made, as well as the fact none of them have
ever had a negative month. Although some people suffer from gambling addiction, it is clearly not
as big of an issue as things like alcohol and tobacco use. It is nice Connecticut is making tax
revenue off of them; hopefully, they put it towards something positive.
"""
)



